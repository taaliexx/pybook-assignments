import requests

from tqdm import tqdm

from homework05.research.age import age_predict
from homework05.research.network import *
from homework05.vkapi.config import VK_CONFIG
from homework05.vkapi.friends import get_friends, get_mutual
from homework05.vkapi.session import Session
from homework05.vkapi.wall import get_wall_execute

domain = VK_CONFIG["domain"]
access_token = VK_CONFIG["access_token"]
v = VK_CONFIG["version"]
user_id = 201430445
fields = 'bdate'

query = f"{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={v}"
response = requests.get(query)
#print(response.json())

s = Session(base_url=VK_CONFIG["domain"], timeout=3)
#print(s.get("get"))

#print(get_friends(201430445))
#print(get_mutual(source_uid=201430445, target_uids=[13980062, 151303866]))
#print(age_predict(user_id=201430445))

friends_response = get_friends(user_id=201430445, fields=["nickname"])
active_users = [user["id"] for user in friends_response.items if not user.get("deactivated")]
#print(len(active_users))
mutual_friends = get_mutual(source_uid=201430445, target_uids=active_users, progress=tqdm)
#print(mutual_friends)

net = ego_network(user_id=201430445)
#plot_ego_network(net)
plot_communities(net)

communities = get_communities(net)
df = describe_communities(communities, friends_response.items, fields=["first_name", "last_name"])
print(df.to_string())

