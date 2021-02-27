import logging, json, addons, random, os, requests, weather2
import chatbot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

temporary = []

#################################################
#              basic global var                 #
#################################################
with open("config.json") as f:
    data = json.loads(f.read())
    token = data["token"]
    user = data["user"]

##################################################
#                     logging                    #
##################################################
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

##################################################
#                support functions               #
##################################################
with open("config.json") as f:
    data = json.loads(f.read())
    USERID = data["userid"]
    allowed = data["allowed"]

def isadmin(user_id, admin_ids=USERID):
    if user_id not in admin_ids: return False
    return True

def enabled(user_id, admin_ids=USERID):
    if user_id not in admin_ids and user_id not in allowed and user_id not in temporary: return False

def error_message():
    answeres = ["Non sei il mio padrone vai via!", "Non sei il mio creatore sparisci!", "Non sono il tuo bot, perciò ti sto per inviare un virus per il tuo smartphone", "Non sono il tuo bot, come mi hai trovato?"]
    return random.choice(answeres)

##################################################
#                admin function                  #
##################################################

def adminpage(update,context):
    ##/admin cmd id
    user_id = update.effective_user.id
    print(str(user_id)+" sta provando ad accedere.")
    try:cmd=context.args[0]
    except: update.message.reply_text("Ma sai come si usa?")
    try: id=int(context.args[1])
    except: id=0
    res=''
    global temporary
    if isadmin(user_id):
        print(str(user_id)+": login.")
        if cmd.lower()=='view':
            if len(temporary)>0:
                res='IDs:\n\n'
                for i in temporary:
                    res+=str(i)+'\n'
            else: res="Zero Temp_Users"
        elif cmd.lower()=='del':
            if len(temporary)>0 and not id == 0:
                if id in temporary:
                    try:temporary.remove(id)
                    except:res='DEL failed'
                    res='DEL done'
                else: res='DEL failed'
        elif cmd.lower()=='add' and not id == 0:
            temporary.append(id)
            res='ADD done'
        else: res="Usage: /admin cmd:<view,add,del> (id)"
    else: res='Non è cazzo tuo'
    update.message.reply_text(res)
    

def broadcast(update,context): #per rompere il cazzo
    user_id = update.effective_user.id
    print(str(user_id)+" sta provando ad accedere.")
    
    global temporary,allowed,USERID, token
    
    u = Updater(token) #usage u.bot. ...
    testo=" ".join(context.args)
    if testo == '':
        update.message.reply_text('Usage: /broadcast + qualsiasi cosa')
        return
    try:
        if isadmin(user_id):
            if len(temporary)>0:
                for i in temporary:
                    try:u.bot.sendMessage(chat_id=i, text=testo)
                    except: print(str(i)+' non ha gradito')
            if len(allowed)>0:
                for i in allowed:
                    try:u.bot.sendMessage(chat_id=i, text=testo)
                    except: print(str(i)+' non ha gradito')
            if len(USERID)>0:
                for i in USERID:
                    try:u.bot.sendMessage(chat_id=i, text=testo)
                    except: print(str(i)+' non ha gradito')
            update.message.reply_text('Broadcast effettuato.')
        else: res='Non è cazzo tuo'
    except: print('Non voglio morire signor Stark')

##################################################
#                conversation                    #
##################################################
'''
Define a few command handlers. These usually take the two arguments update and
context. Error handlers also receive the raised TelegramError object in error.
'''
def start(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text('RILEVATO INTRUSO '+str(user_id)+' : '+error_message())
        return
    response_start = "Ciao sono p.io e sono l'alter ego virtuale di Pio, tipo Jarvis, ma più buggato. Scrivi /help per sapere come crasherò in futuro! :D"
    update.message.reply_text(response_start)

def help(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    """Send a message when the command /help is issued."""
    rep = '''
    Una delle cose che so fare è prevedere i BUS ma solo a Bologna! Cioè se fai /bus NUMEROFERMATA NUMEROLINEA, e puoi anche omettere il nome della linea, posso dirti le cose! E se sei in un'altra città.....niente, il mio potere non funziona li
    Se invece vuoi leggere puoi provare il comando /book + NOME AUTORE e vedere dove porta la tana del bianconiglio.
    Non funziona? Prova /book2 + AUTORE/LIBRO (con o senza /international per le versioni in lingua straniera) 
    Se vuoi l'ignoranza e preferisci vedere una partita scrivi /partite o /partite2 (con o senza squadra o lega o sport che vuoi cercare)
    ATTENZIONE! ti serviranno i DNS di Google (scarica Adguard o vedi su internet come cambiarli)(fai prima da PC)
    Se vuoi tradurre qualcosa per parlare con la tua ragazza ma non capisci una cippa di albanese scrivi /traduttore_albano_romina + FRASE
    Se vuoi cercare un film, artista, serie, autore che potrebbe piacerti, digita /taste + un titolo o un autore, e il bot farà il resto
    Se vuoi cercare qualcosa in streaming, digita /pioflix + il titolo da cercare o /pioflix /ultimeuscite
    Se vuoi sapere il meteo digita /meteo + località italiana
    Se vuoi segnalare un bug digita /segnala + il bug riscontrato
    Se vuoi lamentarti invece vai altrove, sono solo un bot, cazzo vuoi da me?
    '''
    update.message.reply_text(rep)

def taste(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    frase=" ".join(context.args)
    if frase == '':
        update.message.reply_text('Usage: /taste + qualsiasi cosa')
        return
    rep=addons.taste(frase)
    update.message.reply_text(rep)

def traduttore_albano_romina(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    frase=" ".join(context.args)
    if frase == '':
        update.message.reply_text('Usage: /traduttore_albano_romina + frase')
        return
    ret1,ret2=addons.traduttore_albano_romina(frase)
    update.message.reply_text(ret1+"\n"+ret2)

def partite(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    req, lan=addons.calcio()
    if len(req)==0:
        update.message.reply_text("Qualcosa è andato molto storto")
        return
    update.message.reply_text("Ecco gli eventi sportivi richiesti nei prossimi due giorni:")
    def_lan=''
    for i in lan:
        def_lan+=i+'\n'
    #update.message.reply_text(def_lan)
    a=[req[i:i+20] for i in range (0,len(req),20)]
    appoggio=''
    frase=" ".join(context.args)
    if frase == '':
        for items in a:
            for item in items:
                appoggio+=item+'\n'
            update.message.reply_text(appoggio)
            appoggio=''
    else:
        for item in req:
            if frase in item.lower() : appoggio+=item+'\n'
        if appoggio == '':
            update.message.reply_text("Non ho trovato nessun evento sportivo con queste parole")
        update.message.reply_text(appoggio)
        appoggio=''

def partite2(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    req=addons.calcio2() 
    if len(req)==0:
        update.message.reply_text("Qualcosa è andato molto storto")
        return
    update.message.reply_text("Ecco gli eventi sportivi richiesti nei prossimi due giorni:")
    
    a=[req[i:i+20] for i in range (0,len(req),20)]
    appoggio=''
    frase=" ".join(context.args)
    if frase == '':
        for items in a:
            for item in items:
                appoggio+=item+'\n'
            update.message.reply_text(appoggio)
            appoggio=''
    else:
        for item in req:
            if frase in item.lower() : appoggio+=item+'\n'
        if appoggio == '':
            update.message.reply_text("Non ho trovato nessun evento sportivo con queste parole")
        update.message.reply_text(appoggio)
        appoggio=''


def pioflix(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    frase=" ".join(context.args)
    if frase == '':
        update.message.reply_text('Usage: /pioflix + serietv/film/anime')
        return
    if frase == '/ultimeuscite':
        update.message.reply_text('Ecco le ultime uscite/ultimi aggiunti:')
        frase=''
    update.message.reply_text('Searching...')
    req=addons.pioflix(frase)
    if len(req)==0:update.message.reply_text('Non ho trovato nulla :(')
    N_res=4
    a=[req[i:i+N_res] for i in range (0,len(req),N_res)]
    
    appoggio=''
    for items in a:
        for item in items:
            if not 'https:/HD/in' in item and not 'https://www.youtube.com' in item:appoggio+=item+'\n'
        update.message.reply_text(appoggio)
        appoggio=''
    
def answer(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text('RILEVATO INTRUSO '+str(user_id)+' : '+error_message())
        update.message.reply_text('Caro utente '+str(user_id)+', se proprio ci tieni ad entrare, inoltra questo messaggio al mio creatore.\nE già che ci sei digli di aumentarmi la paghetta.')
        print(user_id+" sta provando a messaggiare: "+" ".join(context.args))
        return
    user_says = str(update.message.text)
    response = chatbot.pio.get_response(user_says)
    update.message.reply_text(str(response).capitalize().lower())

def bus(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /bus + fermata {+ linea}')
        return
    """Send a message when the command /bus is issued."""
    fermata = context.args[0]
    try: bus = context.args[1]
    except: bus = 0
    try: query_result = addons.query_hellobus(fermata, bus)
    except: query_result = "Oh oh oh! Hai inserito dei parametri non validi o, molto probabilmente, la linea che cerchi non è servita dal servizio di geolocalizzazione oppure hai inserito dei parametri a cazzo di cane.\nRicorda che il comando corretto è:\n/bus NUMEROFERMATA [NUMEROAUTOBUS]"
    update.message.reply_text(query_result)

def book2(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /book + nome autore o libro')
        return
    try:
        books=addons.zsearch(user_says)
        update.message.reply_text('Searching...')
        for book in books:
            print('B2: Found '+book)
            update.message.reply_text(book)
        update.message.reply_text('A lei, signore!')
    except:
        update.message.reply_text("Sorry, non ho trovato "+user_says.title()+" :(")

def book(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /book + nome autore')
        return
    author = addons.search_author(user_says)
    if author:
        update.message.reply_text("Trovato " + user_says.title() + "! Dammi qualche minuto, ora arriva tutto ciò che hai richiesto!")
        books = addons.wrapper_retrive_books(author)
        for book in books:
            update.message.reply_text(book)
        update.message.reply_text('A lei, signore!')
    else:
        try_author(update,context)
        #update.message.reply_text("Mi dispiace, non ho la più pallida idea di chi sia " + user_says.title() +"! Sicuro tu lo abbia scritto correttamente?")

def try_author(update, context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /try_author + nome e cognome autore')
        return
    author = addons.search_author(user_says)
    if author:
        print("ok")
        #update.message.reply_text("Trovato " + user_says.title() + "! Usa pure la funzione /book")
    else:
        result=addons.try_author(user_says)
        if result:
            author=user_says.replace(' ','-').lower()
            update.message.reply_text("Trovato " + user_says.title() + "! Dammi qualche minuto, ora arriva tutto ciò che hai richiesto!")
            author=[author]
            books = addons.wrapper_retrive_books(author)
            for book in books:
                update.message.reply_text(book)
            update.message.reply_text('A lei, signore!')
        else:
            update.message.reply_text("Sorry, non ho trovato "+user_says.title()+" :(")

def meteo(update,context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /meteo + localita italiana')
        return
    update.message.reply_text(weather2.weather(user_says))
    
def encodec(update,context): #da finire
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /encodec + stringa')
        return
    update.message.reply_text(addons.encodecode(user_says))

def dieta(update,context):
    user_id = update.effective_user.id
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    
    if user_says.lower()=='friarielli':
        update.message.reply_text(addons.dieta_p())
    else:
        update.message.reply_text('Usage: /dieta + password')
        return

def segnala(update,context):
    user_id = update.effective_user.id 
    if enabled(user_id) is False:
        update.message.reply_text(error_message())
        return
    user_says = " ".join(context.args)
    if user_says == '':
        update.message.reply_text('Usage: /segnala + stringa')
        return
    
    global USERID, token
    u = Updater(token)
    try:
        user=update.effective_user.first_name #message.from_user['username'] #update.effective_user.username   first_name
        u.bot.sendMessage(chat_id=USERID[0], text="[[[BUG]]] \nL'utente "+user+"=="+str(user_id)+" segnala: "+user_says)
        update.message.reply_text('Done')
    except: 
        print(str(USERID)+' non ha gradito')
        update.message.reply_text('Error')

##################################################
#                     test                       #
##################################################

def test(update=None, context=None):
    try:
        assert len(addons.dieta_p())>0
        assert len(addons.query_hellobus(str(20)))>0
        assert len(weather2.weather("LOCATION"))>0
        assert len(addons.zsearch(AUTOREDAINSERIRE))>0
        assert addons.try_author(AUTOREDAINSERIRE)==True
        assert len(addons.calcio())>0
        assert len(addons.calcio2())>0
        assert len(addons.traduttore_albano_romina("grazie"))>0
        assert len(addons.taste(SERIEOFILMDAINSERIRE))>0
        assert len(addons.pioflix(SERIEOFILMDAINSERIRE))>0
    except Exception as e:
        if update: update.message.reply_text('Qualcosa non va, guarda i log\n'+e)
        print(e)
    else:
        if update: update.message.reply_text('OK')
        return "OK"

##################################################
#                   bot core                     #
##################################################
def error(update, context):
    '''Log Errors caused by Updates.'''
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def train():
    '''
    with open("chat.txt") as f:
        conversation = f.readlines()
        trainer = ListTrainer(chatbot.taylorchatbot)
        trainer.train(conversation)
    '''
    instance = chatbot.pio
    trainer = ChatterBotCorpusTrainer(instance)
    trainer.train(
        "./corpus/ai.yml",
        "./corpus/botprofile.yml",
        "./corpus/computers.yml",
        "./corpus/conversations.yml",
        "./corpus/emotion.yml",
        "./corpus/food.yml",
        "./corpus/gossip.yml",
        "./corpus/greetings.yml",
        "./corpus/health.yml",
        "./corpus/history.yml",
        "./corpus/humor.yml",
        "./corpus/literature.yml",
        "./corpus/money.yml",
        "./corpus/politics.yml",
        "./corpus/psychology.yml",
        "./corpus/science.yml",
        "./corpus/sports.yml",
        "./corpus/trivia.yml"
    )
    trainer.train('chatterbot.corpus.italian')


def main():
    train() 
    '''Start the bot.
    Create the Updater and pass it your bot's token.
    Make sure to set use_context=True to use the new context based callbacks
    Post version 12 this will no longer be necessary
    '''
    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start)) 
    dp.add_handler(CommandHandler("bus", bus)) 
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("book", book))
    dp.add_handler(CommandHandler("book2", book2))
    dp.add_handler(CommandHandler("meteo", meteo))
    dp.add_handler(CommandHandler("partite", partite))
    dp.add_handler(CommandHandler("partite2", partite2))
    dp.add_handler(CommandHandler("admin", adminpage))
    dp.add_handler(CommandHandler("traduttore_albano_romina", traduttore_albano_romina))
    dp.add_handler(CommandHandler("taste", taste))
    dp.add_handler(CommandHandler("pioflix", pioflix))
    dp.add_handler(CommandHandler("broadcast", broadcast))
    dp.add_handler(CommandHandler("dieta", dieta))
    dp.add_handler(CommandHandler("segnala", segnala))
    dp.add_handler(CommandHandler("test", test))
    #dp.add_handler(CommandHandler("encodec", encodec))
    

    # on noncommand i.e message - answer the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, answer))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

##################################################
#                 end bot core                   #
##################################################


if __name__ == '__main__':
    main()
