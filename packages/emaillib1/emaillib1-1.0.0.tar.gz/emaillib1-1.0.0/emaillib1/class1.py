import smtplib


apple = 'smtp.mail.me.com'
gmail = 'smtp.gmail.com'
yahoo = 'smtp.mail.yahoo.com'
port = 587


class email():
  
  class gmail():
  
    def start():
      try:
        global server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        return f'Connected to {gmail} on port {port} '
      
      except Exception as e:
        return e
    
    def login(user, pssrd):
      server.login(user, pssrd)   
      return l
    
    def send_email(to, sub, message):
      mssg = 'Subject: {}\n\n{}'.format(sub, message)
      server.sendmail('', to, mssg)
      return s
    
    
  class icloud():
    def start():
      try:
        global server2
        server2 = smtplib.SMTP('smtp.mail.me.com', 587)
        server2.starttls()
        return f'Connected to {apple} on port {port} ' 
      
      except Exception as e:
        return e
    
    def login(user, pssrd):
      server2.login(user, pssrd)   
      return l
    
    def send_email(to, sub, message):
      mssg = 'Subject: {}\n\n{}'.format(sub, message)
      server2.sendmail('', to, mssg)
      return s
      
      
  class yahoo():
    
    def start():
      try:
        global server3
        server3 = smtplib.SMTP(yahoo, 587)
        server3.starttls()
        return f'Connected to {yahoo} on port {port} ' 
      
      except Exception as e:
        return e
        
      
    def login(user, pssrd):
      server3.login(user, pssrd)   
      return l
    
    def send_email(to, sub, message):
      mssg = 'Subject: {}\n\n{}'.format(sub, message)
      server3.sendmail('', to, mssg)
      return s
      


