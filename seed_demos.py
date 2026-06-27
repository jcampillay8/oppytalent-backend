import os
import json
import glob
import csv
import uuid

# Argon2 hash for "OppyDemo123!"
DUMMY_PASSWORD_HASH = "$argon2id$v=19$m=65536,t=3,p=4$vBdiLGUspXSulRKidC7l/A$vwkpc1phF7VpnDavco7Zl79BrdydfIo8LdZ5dXZUpxA"

def clean_json_str(content):
    has_header = False
    if content.startswith("jsonb_pretty"):
        has_header = True
        content = content.split('\n', 1)[1].strip()
        
    if content.startswith('"') and content.endswith('"'):
        json_str = content[1:-1].replace('""', '"')
    else:
        json_str = content
    return json_str

def escape_sql(val):
    if val is None:
        return 'NULL'
    if isinstance(val, str):
        return "'" + val.replace("'", "''") + "'"
    return str(val)

def main():
    files = glob.glob("../Data/demo/*_CV.csv")
    files.sort()

    with open('seed.sql', 'w', encoding='utf-8') as out:
        out.write("BEGIN;\n")
        out.write("SET CONSTRAINTS ALL DEFERRED;\n")
        
        for file_path in files:
            print(f"Generating SQL for {file_path}...")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            json_str = clean_json_str(content)
            data = json.loads(json_str)
            perfil = data.get("perfil", {})
            email = perfil.get("email", "")
            
            if "@demo.oppytalent.com" in email:
                profesion = email.split('@')[0]
                username = f"demo-{profesion}"
            else:
                profesion = perfil.get("ocupacion", "profesional").lower().replace(" ", "-")
                username = f"demo-{profesion}"

            user_id = str(uuid.uuid4())
            
            out.write(f"DELETE FROM oppy.usuarios WHERE username = '{username}';\n")
            out.write(f"""INSERT INTO oppy.usuarios 
                (id, username, email, hashed_password, role, is_active, is_deleted, has_accepted_terms, 
                is_recruiter, is_visible_b2b, is_premium, ai_credits, storage_used, failed_login_attempts, ai_pitch_rules, first_name, last_name)
                VALUES ('{user_id}', '{username}', '{email}', '{DUMMY_PASSWORD_HASH}', 'VIEWER', true, false, true, false, false, false, 10, 0, 0, '[]'::json, {escape_sql(perfil.get('first_name'))}, {escape_sql(perfil.get('last_name'))});\n""")
            
            perfil_id = str(uuid.uuid4())
            out.write(f"""INSERT INTO oppy.perfiles 
                (id, usuario_id, email, nombre_completo, ocupacion, descripcion, avatar_url, 
                telefono, linkedin, github, youtube_url, ciudad, certificaciones, idiomas, habilidades, is_active)
                VALUES ('{perfil_id}', '{user_id}', '{email}',
                {escape_sql(perfil.get('nombre_completo'))}, {escape_sql(perfil.get('ocupacion'))}, {escape_sql(perfil.get('descripcion'))},
                {escape_sql(perfil.get('avatar_url'))}, {escape_sql(perfil.get('telefono'))}, {escape_sql(perfil.get('linkedin'))},
                {escape_sql(perfil.get('github'))}, {escape_sql(perfil.get('youtube_url'))}, {escape_sql(perfil.get('ciudad'))},
                {escape_sql(json.dumps(perfil.get('certificaciones', [])))}, {escape_sql(json.dumps(perfil.get('idiomas', [])))},
                {escape_sql(json.dumps(perfil.get('habilidades', [])))}, true);\n""")
            
            for exp in data.get("experiencias", []):
                out.write(f"""INSERT INTO oppy.experiencias 
                    (id, usuario_id, empresa, rol, periodo_inicio, periodo_fin, descripcion_logros, tags_industria, is_active)
                    VALUES ('{str(uuid.uuid4())}', '{user_id}', {escape_sql(exp.get('empresa'))}, {escape_sql(exp.get('rol'))},
                    {escape_sql(exp.get('periodo_inicio'))}, {escape_sql(exp.get('periodo_fin'))}, {escape_sql(exp.get('descripcion_logros'))},
                    {escape_sql(json.dumps(exp.get('tags_industria', [])))}, true);\n""")
                
            for est in data.get("estudios", []):
                out.write(f"""INSERT INTO oppy.estudios 
                    (id, usuario_id, institucion, titulo, anio_obtencion, descripcion_detallada, link, is_active)
                    VALUES ('{str(uuid.uuid4())}', '{user_id}', {escape_sql(est.get('institucion'))}, {escape_sql(est.get('titulo'))},
                    {escape_sql(est.get('anio_obtencion'))}, {escape_sql(est.get('descripcion_detallada'))}, {escape_sql(est.get('link'))}, true);\n""")
                
            for proy in data.get("proyectos", []):
                out.write(f"""INSERT INTO oppy.proyectos 
                    (id, usuario_id, titulo, descripcion_corta, descripcion_detallada, stack_tecnologico, kpis, tags, link_github, link_demo, youtube_url, fecha_proyecto, is_active)
                    VALUES ('{str(uuid.uuid4())}', '{user_id}', {escape_sql(proy.get('titulo'))}, {escape_sql(proy.get('descripcion_corta'))},
                    {escape_sql(proy.get('descripcion_detallada'))}, {escape_sql(json.dumps(proy.get('stack_tecnologico', [])))},
                    {escape_sql(json.dumps(proy.get('kpis', [])))}, {escape_sql(json.dumps(proy.get('tags', [])))},
                    {escape_sql(proy.get('link_github'))}, {escape_sql(proy.get('link_demo'))}, {escape_sql(proy.get('youtube_url'))}, CURRENT_DATE, true);\n""")
                
            for rec in data.get("reconocimientos", []):
                out.write(f"""INSERT INTO oppy.reconocimientos 
                    (id, usuario_id, tipo, titulo, institucion, fecha, descripcion, referencia, is_active)
                    VALUES ('{str(uuid.uuid4())}', '{user_id}', {escape_sql(rec.get('tipo'))}, {escape_sql(rec.get('titulo'))},
                    {escape_sql(rec.get('institucion'))}, {escape_sql(rec.get('fecha'))}, {escape_sql(rec.get('descripcion'))}, {escape_sql(rec.get('referencia'))}, true);\n""")
                
            for hab in data.get("habilitaciones", []):
                out.write(f"""INSERT INTO oppy.habilitaciones 
                    (id, usuario_id, tipo, titulo, descripcion, enlace, is_active)
                    VALUES ('{str(uuid.uuid4())}', '{user_id}', {escape_sql(hab.get('tipo'))}, {escape_sql(hab.get('titulo'))},
                    {escape_sql(hab.get('descripcion'))}, {escape_sql(hab.get('enlace'))}, true);\n""")
                    
        out.write("COMMIT;\n")

    print("seed.sql generated successfully!")

if __name__ == "__main__":
    main()
