import redis

r = redis.Redis(host='localhost', port=6379)

r.set('panda', 'bamboo')
r.set('eel', 'seaweed')
r.set('mako', '12')
r.set('7', 'banana')
r.set('10', '4')
r.set('animals', '["panda","lemming","sheep"]')
r.set('user1', '{ "name": "Sea", "age": 3542, "birthday": "1/32/-1500" }')

print('panda:', r.get('panda').decode('utf-8'))
print('eel:', r.get('eel').decode('utf-8'))
print('mako:', r.get('mako').decode('utf-8'))
print('7:', r.get('7').decode('utf-8'))
print('10:', r.get('10').decode('utf-8'))
print('animals:', r.get('animals').decode('utf-8'))
print('user1:', r.get('user1').decode('utf-8'))

# it only lets you do string representation :(