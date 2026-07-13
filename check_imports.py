print("正在检查所有导入...")

try:
    from app import app, db
    print("✅ app.py 导入正常")
except Exception as e:
    print(f"❌ app.py 导入失败: {e}")

try:
    from ai_routes import ai_bp
    print("✅ ai_routes.py 导入正常")
except Exception as e:
    print(f"❌ ai_routes.py 导入失败: {e}")

try:
    from profile_routes import profile_bp
    print("✅ profile_routes.py 导入正常")
except Exception as e:
    print(f"❌ profile_routes.py 导入失败: {e}")

try:
    from resource_routes import resource_bp
    print("✅ resource_routes.py 导入正常")
except Exception as e:
    print(f"❌ resource_routes.py 导入失败: {e}")

try:
    from path_routes import path_bp
    print("✅ path_routes.py 导入正常")
except Exception as e:
    print(f"❌ path_routes.py 导入失败: {e}")

try:
    from views.ai_views import views_bp
    print("✅ views/ai_views.py 导入正常")
except Exception as e:
    print(f"❌ views/ai_views.py 导入失败: {e}")

try:
    from services.rag_service import rag_chat
    print("✅ services/rag_service.py 导入正常")
except Exception as e:
    print(f"❌ services/rag_service.py 导入失败: {e}")

try:
    from profile_agent import extract_profile
    print("✅ profile_agent.py 导入正常")
except Exception as e:
    print(f"❌ profile_agent.py 导入失败: {e}")

print("检查完成！")