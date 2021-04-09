from beem import Hive
from beem.account import Account
import beem.discussions as discussions
from beem.vote import ActiveVotes
from beem.transactionbuilder import TransactionBuilder
from beembase.operations import Vote
import os
import pickle
import datetime

try:
  with open("state.pickle", "rb") as f:
    state = pickle.load(f)
except:
  state = {"votos": [], "last_called": datetime.datetime.now()}

votos = state["votos"]

if len(votos) > 0:
  print("Último voto: ", votos[-1])
  print("Tiempo: ", datetime.datetime.now());
  if votos[-1]["time"] > datetime.datetime.now() - datetime.timedelta(minutes=30):
    print("último voto en menos de 30 minutos")
    exit()

_2days = datetime.timedelta(days=2)
_5mins = datetime.timedelta(minutes=2)
dryrun = False
account = os.getenv("hiveaccount")
user = Account(account)
pkey = os.getenv("postingkey")
with open("cuentas", "r") as f:
  cuentas = [s.strip() for s in f.readlines()]


  
hive = Hive(keys=[pkey])
weight = 100
votado = False

for cuenta in cuentas:
  print("Cuenta ", cuenta)
  #  q = Query(limit=2, tag=cuenta)
  for h in discussions.Discussions_by_author_before_date(cuenta, limit=1):
    print("Post https://hive.blog/@"  + cuenta + "/" + h.permlink, h["created"])
    age = h.time_elapsed()
    if age > _2days or age < _5mins: 
      print("Skipping")
      continue
    mivoto = h.get_vote_with_curation(account, raw_data=True)
    if mivoto is None:
      print("Votando")
      
      tx = TransactionBuilder(blockchain_instance=hive)
      tx.appendOps(Vote(**{
        "voter": account,
        "author": cuenta,
        "permlink": h.permlink,
        "weight": int(float(weight) * 100)
      }))

      tx.appendWif(pkey)
      signed_tx = tx.sign()
      if not dryrun:
        broadcast_tx = tx.broadcast(trx_id=True)
      
      votado = True
      votos.append({
          "time": datetime.datetime.now(),
          "permlink": h.permlink,
          "rewards": h.get_rewards()
        })
      print(votos[-1])
  if votado is True:
    break
  
with open("state.pickle", "wb") as f:
  state["votos"] = votos
  state["last_called"] = datetime.datetime.now()
  pickle.dump(state, f)

exit()
