import fire
import asyncio
import random
import os
import string
import logging
from aiohttp import web

HOST = "http://pastes.lan"
PATH = '/tmp/serve'

routes = web.RouteTableDef()

CHARSET = string.ascii_lowercase+string.digits
def rstr(leng):
  return ''.join(random.choice(CHARSET) for _ in range(leng))

@routes.post('/submit')
async def submit_post(request):
    '''
    {
        'paste': 'txt_data'
    }
    '''
    uid = rstr(random.randint(5, 8))
    loc = os.path.join(PATH, uid+'.txt')
    
    data = await request.post()

    filename = data['paste'].filename
    input_file = data['paste'].file
    
    content = input_file.read()

    with open(loc, 'wb') as fd:
      fd.write(content)
    logging.info(f"Created {PATH}/{uid}.txt")
    return web.Response(body=f"{HOST}/raw/{uid}")


@routes.get('/raw/{id}')
async def get_post(request):
    uid = request.match_info['id']
    loc = os.path.join(PATH, uid+'.txt')
    
    if not os.path.exists(loc):
        return web.Response(status=404)

    with open(loc, 'r') as fd:
        return web.Response(body=fd.read())

async def setup(webapp, port, interface):
  runner = web.AppRunner(webapp)
  await runner.setup()
  
  site = web.TCPSite(runner, host=interface, port=port, reuse_address=True)
  await site.start()

def main(serve="/tmp/pastes", log=None, port=8080, interface="0.0.0.0"):
  global PATH
  PATH=serve
  
  logging

  if log:
    log_args = {'filename': log, 'level': logging.INFO, 'filemode': 'a'}
  else:
    log_args = {'level': logging.INFO}

  logging.basicConfig(**log_args)

  app = web.Application()
  app.add_routes(routes)

  if not os.path.exists(PATH):
    os.makedirs(PATH, exist_ok=True)

  loop = asyncio.get_event_loop()

  loop.create_task(setup(app, interface=interface, port=port))

  #loop.run_until_complete(loop.create_server())
  print(f"Running webserver API at http://{interface}:{port} [{serve}]")
  
  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass

if __name__ == '__main__':
  fire.Fire(main)