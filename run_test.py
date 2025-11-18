from test import ModuleBasedAppBuilder
import os
builder = ModuleBasedAppBuilder(api_key=os.getenv("GEMINI_API_KEY"))
builder.build_app("build a  basic user account management app: register/login users, persist profiles, edit profile details, and sync to Firebase.")