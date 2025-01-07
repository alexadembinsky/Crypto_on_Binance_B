import inspect
import os
from datetime import datetime
from config import TRACING_ENABLED

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(PROJECT_ROOT)


def trace_function_call():
    if TRACING_ENABLED:
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        parent_frame = caller_frame.f_back if caller_frame else None

        current_function_name = caller_frame.f_code.co_name if caller_frame else "Unknown"
        parent_function_name = parent_frame.f_code.co_name if parent_frame else "Global Scope"

        # Получаем аргументы функции
        args_info = inspect.getargvalues(caller_frame)

        # Формируем строку с позиционными аргументами
        args = [f"{arg}={args_info.locals[arg]!r}" for arg in args_info.args]

        # Добавляем *args если есть
        if args_info.varargs and args_info.locals[args_info.varargs]:
            args.append(f"*{args_info.varargs}={args_info.locals[args_info.varargs]!r}")

        # Добавляем **kwargs если есть
        if args_info.keywords and args_info.locals[args_info.keywords]:
            args.append(f"**{args_info.keywords}={args_info.locals[args_info.keywords]!r}")

        # Собираем все аргументы в строку
        args_str = ", ".join(args)

        # Получаем полный путь к файлу
        full_file_path = caller_frame.f_code.co_filename

        # Преобразуем в относительный путь
        try:
            relative_path = os.path.relpath(full_file_path, PROJECT_ROOT)
        except ValueError:
            # Если файл находится на другом диске, оставляем полный путь
            relative_path = full_file_path

        line_number = caller_frame.f_lineno
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{timestamp}] Функция {current_function_name} "
              f"(файл: {relative_path}, строка: {line_number}) "
              f"вызвана из {parent_function_name}\n"
              f"Аргументы: {args_str}")

        del current_frame
        del caller_frame
        del parent_frame
