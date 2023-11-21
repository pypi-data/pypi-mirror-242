import os

if __name__ == '__main__':
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".py") and file != "__init__.py" and file != "generate_xml.py":
                # 输出文件名
                name = file.replace(".py", "")
                print(f'<{name} modulePath="pyodm.model.v2.cdisc.{name}" clazz="{name}"/>')
