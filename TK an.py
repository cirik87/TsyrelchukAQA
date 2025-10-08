# -*- coding: utf-8 -*-
import sys
import re
import json
import os
import getpass
import argparse
from typing import Dict, List, Optional, Tuple, Set
import requests
from bs4 import BeautifulSoup
import urllib3
from urllib3.exceptions import InsecureRequestWarning

MIN_NAME_LEN = 10
MAX_NAME_LEN = 120

# Слова, нежелательные в названиях ТК (для оценки качества имен)
DEFAULT_BLACKLIST = {"test", "тест", "temp", "draft", "copy", "копия", "sample", "пример"}

# Карта модулей → ключевые слова (для логической группировки по описанию)
DEFAULT_MODULE_KEYWORDS = {
    "НСИ": {"нси", "справочник", "классификатор"},
    "Платежи": {"платеж", "оплата", "касса", "чек"},
    "ЛК": {"личный кабинет", "профиль", "авторизация", "вход"},
}

def normalize_name(name: Optional[str]) -> str:
    return (name or "").strip().lower()

def evaluate_name_quality(
    name: str,
    min_len: int = MIN_NAME_LEN,
    max_len: int = MAX_NAME_LEN,
    blacklist: Optional[Set[str]] = None,
) -> Tuple[bool, List[str]]:
    reasons: List[str] = []
    trimmed = name.strip()
    words = [w for w in re.split(r"[\s_/:-]+", trimmed) if w]
    blacklist = blacklist or DEFAULT_BLACKLIST

    if len(trimmed) < min_len:
        reasons.append(f"слишком короткое (<{min_len})")
    if len(trimmed) > max_len:
        reasons.append(f"слишком длинное (>{max_len})")
    if not trimmed[:1].isupper():
        reasons.append("должно начинаться с заглавной буквы")
    if len(words) < 2:
        reasons.append("слишком мало слов (<2)")
    if any(normalize_name(w) in blacklist for w in words):
        reasons.append("содержит запрещённые слова (test/тест/temp/draft/copy/копия)")

    return (len(reasons) == 0), reasons

class ZephyrScaleClient:
    """
    Универсальный клиент для Zephyr Scale (TM4J) Server/DC и Zephyr Squad.
    Работает через Jira base URL. Пытается:
    - list_folders: собрать список папок (через кейсы или известные эндпоинты)
    - list_test_cases_project: постранично выкачать все кейсы проекта
    - list_test_cases_by_folder: отфильтровать по folder.id
    - get_html: запрос HTML для fallback-скрейпинга
    - login_session: создать сессию (куки), если basic недостаточно
    """
    def __init__(
        self,
        jira_base_url: str,
        email: str,
        api_token: str,
        timeout_sec: int = 30,
        verify_ssl: bool = True,
        debug: bool = False,
    ):
        self.jira_base_url = jira_base_url.rstrip("/")
        self.timeout_sec = timeout_sec
        self.verify_ssl = verify_ssl
        self.debug = debug
        self.session = requests.Session()
        self.session.auth = (email, api_token)
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
            "Accept": "application/json, text/plain, */*",
        })

    def _get(self, url: str, params: Optional[Dict] = None, expect_json=True):
        try:
            resp = self.session.get(url, params=params, timeout=self.timeout_sec, verify=self.verify_ssl)
        except requests.exceptions.SSLError:
            if self.verify_ssl:
                resp = self.session.get(url, params=params, timeout=self.timeout_sec, verify=False)
            else:
                raise
        if resp.status_code >= 400:
            raise RuntimeError(f"GET {url} -> {resp.status_code} {resp.text[:500]}")
        return resp.json() if expect_json else resp.text

    def get_html(self, url: str) -> str:
        return self._get(url, expect_json=False)

    def login_session(self, username: Optional[str], password: Optional[str]) -> bool:
        # Пытаемся REST-сессию (для некоторых инсталляций Jira)
        rest_url = f"{self.jira_base_url}/rest/auth/1/session"
        payload = {"username": username, "password": password}
        headers_json = {"Content-Type": "application/json"}
        try:
            if self.debug:
                print(f"[DEBUG] Try REST session {rest_url}")
            try:
                r = self.session.post(rest_url, json=payload, headers=headers_json, timeout=self.timeout_sec, verify=self.verify_ssl)
            except requests.exceptions.SSLError:
                r = self.session.post(rest_url, json=payload, headers=headers_json, timeout=self.timeout_sec, verify=False)
            if 200 <= r.status_code < 300:
                if self.debug:
                    print("[DEBUG] REST session OK")
                return True
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] REST session error: {e}")
        # Форма логина
        try:
            login_page = f"{self.jira_base_url}/login.jsp"
            r1 = self.session.get(login_page, timeout=self.timeout_sec, verify=self.verify_ssl)
            token = None
            os_destination = "/secure/MyJiraHome.jspa"
            if r1.status_code < 400:
                soup = BeautifulSoup(r1.text, "html.parser")
                t = soup.find("input", attrs={"name": "atl_token"}) or soup.find("input", attrs={"name": "os_security_token"})
                if t and t.get("value"):
                    token = t["value"]
                d = soup.find("input", attrs={"name": "os_destination"})
                if d and d.get("value"):
                    os_destination = d["value"]
            form_data = {
                "os_username": username,
                "os_password": password,
                "os_cookie": "true",
                "os_destination": os_destination,
                "login": "Log In",
            }
            if token:
                form_data["atl_token"] = token
                form_data["os_security_token"] = token
            r2 = self.session.post(f"{self.jira_base_url}/login.jsp", data=form_data, timeout=self.timeout_sec, verify=self.verify_ssl)
            r3 = self.session.get(f"{self.jira_base_url}/secure/Dashboard.jspa", timeout=self.timeout_sec, verify=self.verify_ssl)
            return r3.status_code < 400 and "Forbidden" not in r3.text
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Form login error: {e}")
            return False

    def list_test_cases_project(self, project_ref: str) -> List[Dict]:
        """
        Универсальная выгрузка всех ТК проекта (Zephyr Squad: /rest/tests/1.0/testcase).
        Для Scale DC можно также настроить другие эндпоинты, но часто кейсы доступны в /rest/tests/1.0/testcase.
        """
        collected: List[Dict] = []
        start_at = 0
        page_size = 200
        url = f"{self.jira_base_url}/rest/tests/1.0/testcase"
        while True:
            params = {"startAt": start_at, "maxResults": page_size}
            if str(project_ref).isdigit():
                params["projectId"] = int(project_ref)
            else:
                params["projectKey"] = project_ref
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout_sec, verify=self.verify_ssl)
            except requests.exceptions.SSLError:
                resp = self.session.get(url, params=params, timeout=self.timeout_sec, verify=False)
            if resp.status_code >= 400:
                raise RuntimeError(f"GET {url} -> {resp.status_code} {resp.text[:400]}")
            data = resp.json()
            values = data if isinstance(data, list) else (data.get("values") or data.get("results") or [])
            collected.extend(values)
            if not values or len(values) < page_size:
                break
            start_at += len(values)
        return collected

    def list_folders(self, project_ref: str) -> List[Dict]:
        """
        Пытается получить папки:
        1) Через кейсы проекта (надёжный способ)
        2) Через известные эндпоинты (если доступны)
        """
        try:
            cases = self.list_test_cases_project(project_ref)
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] list_test_cases_project failed: {e}")
            cases = []
        folders = []
        seen = set()
        for tc in cases:
            folder = tc.get("folder") or {}
            fid = folder.get("id")
            fpath = folder.get("fullPath") or folder.get("name")
            pid = folder.get("parentId")
            key = (fid, fpath)
            if fpath and key not in seen:
                seen.add(key)
                folders.append({
                    "id": fid,
                    "name": (fpath.split("/")[-1] if isinstance(fpath, str) else fpath),
                    "parentId": pid,
                    "fullPath": fpath,
                })
        if folders:
            return folders
        # fallback: известные эндпоинты (если доступны в вашей инсталляции)
        for path in [
            "/rest/tests/1.0/folder",
            "/rest/tests/1.0/folder/tree",
            "/rest/tests/1.0/testrepository/folders",
            "/rest/tests/1.0/testrepository/folders/tree",
        ]:
            try:
                url = f"{self.jira_base_url}{path}"
                params = {"projectKey": project_ref} if not str(project_ref).isdigit() else {"projectId": int(project_ref)}
                r = self.session.get(url, params=params, timeout=self.timeout_sec, verify=self.verify_ssl)
                if r.status_code < 400:
                    data = r.json()
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict):
                        values = data.get("values") or data.get("results") or data.get("folders") or []
                        if values:
                            return values
            except Exception:
                continue
        return []

    def list_test_cases_by_folder(self, project_ref: str, folder_id: Optional[int]) -> List[Dict]:
        """
        Фильтрует кейсы проекта по folder.id (набор уже выгружен).
        """
        cases = self.list_test_cases_project(project_ref)
        out = []
        for c in cases:
            folder = c.get("folder") or {}
            if folder.get("id") == folder_id:
                out.append(c)
        return out

def build_folder_index(folders: List[Dict]) -> Tuple[Dict[int, Dict], Dict[Optional[int], List[int]]]:
    id_to_folder: Dict[int, Dict] = {}
    parent_to_children: Dict[Optional[int], List[int]] = {}
    for f in folders:
        fid = f.get("id")
        pid = f.get("parentId")
        id_to_folder[fid] = f
        parent_to_children.setdefault(pid, []).append(fid)
    return id_to_folder, parent_to_children

def resolve_folder_path(path: str, id_to_folder: Dict[int, Dict], parent_to_children: Dict[Optional[int], List[int]]) -> Optional[int]:
    parts = [p.strip() for p in path.split("/") if p.strip()]
    if not parts:
        return None
    # попытка точного совпадения fullPath
    for fid, f in id_to_folder.items():
        full_path = f.get("fullPath") or f.get("path")
        if full_path and normalize_name(full_path) == normalize_name(path):
            return fid
    # По уровням
    candidates = parent_to_children.get(None, [])
    for part in parts:
        next_candidates: List[int] = []
        for fid in candidates:
            child_ids = parent_to_children.get(fid, [])
            for cid in child_ids:
                if normalize_name(id_to_folder[cid].get("name")) == normalize_name(part):
                    next_candidates.append(cid)
        if not next_candidates:
            fallback = [fid for fid, f in id_to_folder.items() if normalize_name(f.get("name")) == normalize_name(part)]
            if len(fallback) == 1:
                candidates = fallback
                continue
            return None
        candidates = next_candidates
    return candidates[0] if candidates else None

def collect_descendants(root_id: int, parent_to_children: Dict[Optional[int], List[int]]) -> Set[int]:
    result: Set[int] = {root_id}
    stack = [root_id]
    while stack:
        cur = stack.pop()
        for child in parent_to_children.get(cur, []):
            if child not in result:
                result.add(child)
                stack.append(child)
    return result

def extract_description(testcase: Dict) -> str:
    desc = testcase.get("description") or testcase.get("objective") or testcase.get("definition") or ""
    # также пробуем customFields
    cfs = testcase.get("customFields")
    if not desc and isinstance(cfs, list):
        for cf in cfs:
            name = (cf.get("name") or "").strip().lower()
            if name in {"описание", "description", "objective"}:
                val = cf.get("values") or cf.get("value")
                if isinstance(val, list) and val:
                    desc = str(val[0])
                elif isinstance(val, str):
                    desc = val
                if desc:
                    break
    # HTML → текст
    return BeautifulSoup(desc, "html.parser").get_text(" ", strip=True)

def classify_module(description: str, module_keywords: Dict[str, Set[str]]) -> str:
    text = (description or "").lower()
    for module, kws in module_keywords.items():
        for kw in kws:
            if kw in text:
                return module
    return "Другое"

def group_cases(cases: List[Dict], group_field: str, module_keywords: Dict[str, Set[str]]) -> Dict[str, List[Dict]]:
    """
    Логическая группировка:
    - По стандартным полям (priority, status, owner.displayName, component.name, labels, folder.fullPath)
    - По кастомному полю (customFields[].name == group_field)
    - По описанию: group_field == 'description' → группировка по очищенному описанию
    - По модулю: group_field == 'module' → классификация по ключевым словам описания
    """
    key = group_field.strip().lower()
    groups: Dict[str, List[Dict]] = {}

    for tc in cases:
        value = None
        if key in ("priority", "status"):
            raw = tc.get(key)
            value = raw.get("name") if isinstance(raw, dict) else (raw or "")
        elif key in ("owner", "assignee"):
            owner = tc.get("owner") or tc.get("assignee")
            value = (owner.get("displayName") or owner.get("name")) if isinstance(owner, dict) else (owner or "")
        elif key in ("component", "components"):
            comp = tc.get("component") or (tc.get("components")[0] if isinstance(tc.get("components"), list) and tc.get("components") else None)
            value = comp.get("name") if isinstance(comp, dict) else (comp or "")
        elif key in ("label", "labels", "tag", "tags"):
            labels = tc.get("labels") or tc.get("tags") or []
            value = ", ".join(sorted(set(labels))) if isinstance(labels, list) else str(labels or "")
        elif key in ("folder", "folder_path", "path"):
            folder = tc.get("folder") or {}
            value = folder.get("fullPath") or folder.get("name") or ""
        elif key in ("description", "objective", "definition"):
            value = extract_description(tc)
        elif key in ("module", "модуль"):
            desc = extract_description(tc)
            value = classify_module(desc, module_keywords)
        else:
            # попытка найти кастомное поле по имени
            cfs = tc.get("customFields")
            if isinstance(cfs, list):
                for cf in cfs:
                    if normalize_name(cf.get("name")) == key:
                        val = cf.get("values") or cf.get("value")
                        if isinstance(val, list):
                            value = ", ".join(map(str, val))
                        else:
                            value = str(val or "")
                        break
            if value is None:
                # если не нашли, пробуем прямой ключ на верхнем уровне
                raw = tc.get(group_field)
                if isinstance(raw, dict):
                    value = raw.get("name") or raw.get("value") or str(raw)
                elif isinstance(raw, list):
                    value = ", ".join(map(str, raw))
                else:
                    value = str(raw or "")

        value = value if (value is not None and str(value).strip()) else "(не указано)"
        groups.setdefault(str(value), []).append(tc)

    return groups

def export_groups_to_txt(
    filepath: str,
    groups: Dict[str, List[Dict]],
    title: str,
    folder_path: str,
    group_field: str,
    top_n_per_group: int = 200,
) -> None:
    lines: List[str] = []
    total = sum(len(v) for v in groups.values())
    # Заголовок
    lines.append("=" * 90)
    lines.append(title)
    lines.append("=" * 90)
    lines.append(f"Папка: {folder_path}")
    lines.append(f"Поле группировки: {group_field}")
    lines.append(f"Всего тест-кейсов: {total}")
    lines.append(f"Всего групп: {len(groups)}")
    lines.append("")

    # Сводка по группам (по убыванию размера)
    lines.append("Сводка по группам:")
    for gname, items in sorted(groups.items(), key=lambda t: len(t[1]), reverse=True):
        lines.append(f" - {gname}: {len(items)}")
    lines.append("")

    # Детальный блок
    for gname, items in sorted(groups.items(), key=lambda t: len(t[1]), reverse=True):
        lines.append("-" * 90)
        lines.append(f"[Группа] {gname} — {len(items)} кейсов")
        lines.append("-" * 90)
        for it in items[:top_n_per_group]:
            key = it.get("key") or str(it.get("id") or "")
            name = it.get("name") or ""
            lines.append(f" • {key}: {name}")
        if len(items) > top_n_per_group:
            lines.append(f"   ... и еще {len(items) - top_n_per_group} кейсов")
        lines.append("")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def parse_project_from_url(any_url: str) -> Tuple[Optional[str], Optional[int]]:
    try:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(any_url)
        qs = parse_qs(parsed.query)
        key = None
        pid: Optional[int] = None
        if qs.get("projectKey"):
            key = (qs["projectKey"][0] or "").strip()
        if qs.get("projectId"):
            raw = (qs["projectId"][0] or "").strip()
            if raw.isdigit():
                pid = int(raw)
        path = parsed.path or ""
        if not key:
            m = re.search(r"/browse/([A-Za-z][A-Za-z0-9_]+)-\d+", path)
            if m:
                key = m.group(1).upper()
        if not key:
            m = re.search(r"/(projects|project)/([A-Za-z][A-Za-z0-9_]+)", path)
            if m:
                key = m.group(2).upper()
        if pid is None:
            m = re.search(r"/(projects|project)/(\d+)", path)
            if m:
                try:
                    pid = int(m.group(2))
                except Exception:
                    pid = None
        # fragment (#...) тоже может содержать query
        frag = parsed.fragment or ""
        if frag:
            frag_qs = parse_qs(re.sub(r"^[^?]*\?", "", frag)) if "?" in frag else {}
            if not key and frag_qs.get("projectKey"):
                key = (frag_qs["projectKey"][0] or "").strip()
            if pid is None and frag_qs.get("projectId"):
                raw = (frag_qs["projectId"][0] or "").strip()
                if raw.isdigit():
                    pid = int(raw)
        return key, pid
    except Exception:
        return None, None

def scrape_folders_from_html(html: str) -> List[Dict]:
    folders: List[Dict] = []
    seen = set()
    # JSON-подобные вкрапления
    for m in re.finditer(r"\{[^{}]*\"id\"\s*:\s*(\d+)[^{}]*\"fullPath\"\s*:\s*\"([^\"]+)\"[^{}]*\"parentId\"\s*:\s*(\d+|null)[^{}]*\}", html):
        fid = int(m.group(1))
        full_path = m.group(2)
        parent_raw = m.group(3)
        parent_id = None if parent_raw == "null" else int(parent_raw)
        key = (fid, full_path)
        if key in seen:
            continue
        seen.add(key)
        folders.append({
            "id": fid,
            "name": full_path.split("/")[-1],
            "parentId": parent_id,
            "fullPath": full_path,
        })
    # data-* атрибуты
    for m in re.finditer(r"data-folder-id=\"(\d+)\"[\s\S]{0,200}?data-full-path=\"([^\"]+)\"", html):
        fid = int(m.group(1))
        full_path = m.group(2)
        key = (fid, full_path)
        if key in seen:
            continue
        seen.add(key)
        folders.append({
            "id": fid,
            "name": full_path.split("/")[-1],
            "parentId": None,
            "fullPath": full_path,
        })
    return folders

def analyze_and_export(
    jira_base_url: str,
    url_hint: str,
    email: str,
    api_token: str,
    folder_path: str,
    group_field: str,
    include_subfolders: bool = True,
    export_txt_path: str = "zephyr_analysis.txt",
    insecure_ssl: bool = False,
    debug: bool = False,
    module_keywords_path: Optional[str] = None,
):
    if insecure_ssl:
        try:
            urllib3.disable_warnings(InsecureRequestWarning)
        except Exception:
            pass

    client = ZephyrScaleClient(
        jira_base_url=jira_base_url,
        email=email,
        api_token=api_token,
        verify_ssl=not insecure_ssl,
        debug=debug,
    )

    # Сессия (куки) — полезно для некоторых инсталляций
    client.login_session(email, api_token)

    # Определяем проект
    proj_key, proj_id = parse_project_from_url(url_hint)
    project_ref = proj_key or (str(proj_id) if proj_id else None)
    if not project_ref:
        raise RuntimeError("Не удалось определить ключ/ID проекта из URL. Передайте корректный URL на вашу Jira/Zephyr страницу проекта/репозитория.")

    # Загружаем и строим индекс папок
    folders = client.list_folders(project_ref)
    if not folders:
        # fallback: скрейпинг текущей страницы
        try:
            html = client.get_html(url_hint)
            folders = scrape_folders_from_html(html)
        except Exception:
            folders = []
    id_to_folder, parent_to_children = build_folder_index(folders)

    # Разрешаем путь папки → ID
    normalized_folder_path = folder_path.lstrip("/")
    folder_id = resolve_folder_path(normalized_folder_path, id_to_folder, parent_to_children)
    if folder_id is None:
        top_level = [fid for fid, f in id_to_folder.items() if f.get("parentId") is None]
        suggestions = ", ".join(sorted({id_to_folder[fid]["name"] for fid in top_level}))
        raise RuntimeError(f"Не найдена папка по пути: {folder_path}. Возможные верхнеуровневые: {suggestions}")

    # Собираем все нужные folder_id (учитывая подпапки)
    folder_ids = {folder_id} if not include_subfolders else collect_descendants(folder_id, parent_to_children)

    # Собираем кейсы из каждой папки
    all_cases: List[Dict] = []
    for fid in folder_ids:
        all_cases.extend(client.list_test_cases_by_folder(project_ref, fid))

    # Загружаем карту модулей (если нужна классификация по 'module')
    module_keywords = DEFAULT_MODULE_KEYWORDS
    if module_keywords_path and os.path.isfile(module_keywords_path):
        try:
            raw = json.load(open(module_keywords_path, "r", encoding="utf-8"))
            module_keywords = {k: {str(x).lower() for x in (v or [])} for k, v in raw.items()}
        except Exception:
            pass

    # Группировка
    groups = group_cases(all_cases, group_field=group_field, module_keywords=module_keywords)

    # Экспорт TXT
    export_groups_to_txt(
        filepath=export_txt_path,
        groups=groups,
        title="Отчет по тест-кейсам (Jira Zephyr)",
        folder_path=folder_path,
        group_field=group_field,
    )

    # Краткая консольная сводка
    total = len(all_cases)
    print(f"Всего ТК: {total}")
    print(f"Групп: {len(groups)}")
    print("Топ групп:")
    for gname, items in sorted(groups.items(), key=lambda t: len(t[1]), reverse=True)[:10]:
        print(f" - {gname}: {len(items)}")
    print(f"TXT отчет: {export_txt_path}")

def main():
    parser = argparse.ArgumentParser(description="Анализ ТК в Jira Zephyr: рекурсивный сбор, группировка по полю, экспорт TXT.")
    parser.add_argument("--url", required=True, help="Любая ссылка на Jira/Zephyr в рамках нужного проекта (для определения projectKey/Id)")
    parser.add_argument("--base-url", required=True, help="Базовый URL Jira, например https://jira.company.com")
    parser.add_argument("--email", required=False, help="Логин Jira (email). Если не задано — будет запрошен")
    parser.add_argument("--api-token", required=False, help="Пароль/токен Jira. Если не задано — будет запрошен")
    parser.add_argument("--group-field", required=True, help="Поле группировки (priority/status/owner/component/labels/folder/description/module или имя кастомного поля)")
    parser.add_argument("--include-subfolders", action="store_true", help="Включать подпапки")
    parser.add_argument("--export-txt", default="zephyr_analysis.txt", help="Путь к TXT отчету")
    parser.add_argument("--module-keywords", help="JSON-файл карта модулей → ключевые слова (для group-field=module)")
    parser.add_argument("--insecure", action="store_true", help="Игнорировать SSL (внутренние CA)")
    parser.add_argument("--debug", action="store_true", help="Подробный лог")
    args = parser.parse_args()

    email = args.email or input("Jira email/username: ").strip()
    api_token = args.api_token or getpass.getpass("Jira password/API token: ").strip()

    analyze_and_export(
        jira_base_url=args.base_url,
        url_hint=args.url,
        email=email,
        api_token=api_token,
        folder_path=args.folder_path,
        group_field=args.group_field,
        include_subfolders=args.include_subfolders,
        export_txt_path=args.export_txt,
        insecure_ssl=args.insecure,
        debug=args.debug,
        module_keywords_path=args.module_keywords,
    )

if __name__ == "__main__":
    main()
