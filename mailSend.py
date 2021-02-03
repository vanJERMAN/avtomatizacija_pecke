import umail
def mail(machine, distance, receiver):
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True) # Gmail's SSL port
    smtp.login('HERE GOES SENDER EMAIL', 'HERE GOES SENDER PASSWORD')
    smtp.to(receiver)
    smtp.write("From: {} <home.automation.seca.179@gmail.com>\n".format(machine))
    smtp.write("Subject: Čas je za dofilat pelete!\n\n")
    smtp.write("Kmalu bo zmanjkalo pelet. Razdalja: {}\n".format(distance))
    smtp.send()
    smtp.quit()
