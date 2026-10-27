from auth import init_auth_tables, create_user, login, customer_for_token

init_auth_tables()
create_user("C1", "pass1")
create_user("C2", "pass2")

print("wrong password:", login("C1", "nope"))
token = login("C1", "pass1")
print("token looks like:", token[:8] + "...")
print("who owns this token?", customer_for_token(token))
print("fake token:", customer_for_token("made-up"))