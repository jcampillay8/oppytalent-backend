import os
import glob

routers = [
    "proyectos.py", "experiencias.py", "estudios.py", 
    "reconocimientos.py", "habilitaciones.py", "perfil.py"
]

for router in routers:
    path = f"/home/jcampillay/WorkArea/OppyTalent/OppyTalent-backend/app/api/v1/{router}"
    if not os.path.exists(path): continue
    
    with open(path, "r") as f:
        content = f.read()
        
    # Inject BackgroundTasks import if not present
    if "from fastapi import BackgroundTasks" not in content and "from fastapi import APIRouter" in content:
        content = content.replace("from fastapi import APIRouter", "from fastapi import APIRouter, BackgroundTasks")
    
    # Inject trigger import
    if "from app.ai_management.rag_sync import trigger_rag_sync_background" not in content:
        content = content.replace("from app.models", "from app.ai_management.rag_sync import trigger_rag_sync_background\nfrom app.models")
        
    # Find all async def create_, update_, delete_
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Modify signature
        if line.startswith("async def create_") or line.startswith("async def update_") or line.startswith("async def delete_") or line.startswith("async def save_"):
            if "current_user:" in line and "background_tasks: BackgroundTasks" not in line:
                # Add background_tasks to signature
                # Find the closing parenthesis
                j = i
                while ")" not in lines[j]:
                    j += 1
                lines[j] = lines[j].replace("):", ",\n    background_tasks: BackgroundTasks\n):")
                
        # Inject trigger before return
        if line.strip().startswith("return ") and "await db_session.commit()" in "\n".join(lines[max(0, i-5):i]):
            # Verify we are inside a route that has current_user
            if "current_user" in content:
                # We need to inject the trigger
                indent = line[:len(line) - len(line.lstrip())]
                new_lines.insert(-1, f"{indent}trigger_rag_sync_background(background_tasks, current_user)")
                
        i += 1
        
    with open(path, "w") as f:
        f.write("\n".join(new_lines))

print("Patch applied")
