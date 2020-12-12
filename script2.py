import email_to

server = email_to.EmailServer('smtp.gmail.com', 587, 'jjesuisla774@gmail.com', 'P4t4t3_01')

message = server.message()
message.add('# Oh boy, something went wrong!')
message.add('- The server had a hiccup')
message.add('- The power went out')
message.add('- Blame it on a rogue backhoe')
message.style = 'h1 { color: red}'

message.send('jjesuisla774@gmail.com', 'Things did not occur as expected')