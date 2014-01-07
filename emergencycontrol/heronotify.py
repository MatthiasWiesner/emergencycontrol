from time import sleep
import datetime
from model import Person, EmergencyService
import sendgrid
from emergencycontrol import app

from flask_script import Command


class HeroNotify(Command):

    def run(self):
        while True:
            now = datetime.date.today()
            if now.weekday() == 4:
                monday = now + datetime.timedelta(days=3)
                week = EmergencyService.query \
                    .filter(EmergencyService.start_date == monday) \
                    .first()

                person = Person.query.get(week.person_id)
                data = {'start_date': week.start_date,
                    'end_date': week.end_date,
                    'hero': person.name}

                # make a secure connection to SendGrid
                s = sendgrid.Sendgrid(app.config['SENDGRID_USERNAME'], app.config['SENDGRID_PASSWORD'], secure=True)

                content ="""

Dear {hero},

Baaam! You are the operational ninja hero next week from {start_date} to {end_date}


                 :N/
                mom/
               .M`.m/
               `M- .m/
                od` -m:
                 hs  :m-
                 `do  /m.
                  .m/  +d`
                   -m:  sh`
                    :m-  yy
                     /m. `hs
                      +d` `do
                       sh` .d+               .-/+syyhhhyyss+/:-.`
                        yy` -m:          `-odmMMMMMMMMMMMMMMMMNNmdyo/-.
                        `hs  -m-       `/dMMMMMMMMMMMMMMMMMMMMMMMMMMMNmhs/-`
                         `d+  :m.     .hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNmh+-`
                          .m/  +d.   `dMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMNNmmh+s
                           -m:  od`  -MMMNNNNNNMMMMMNNNNNNNNNNmmmmdhysoo/:-.`  :+
                            :m-  sh` `NMm/:-:::::::::::----...``.-`   /dh+   `+d`
                             /m.  yy  :mMNds:.`                -NMd.  sMMN`.+dN:
                              +d` `hs  .sNMMMMmhs+:.```        -NMm. ``oNmdMMM+
                               od` `d+   .omNMMMMMMMNmdhyyssoooohNyyhmNMMMMMN/
                                yh  .m/     -odNMMMMMMMMMMMMMMMMMMMMMMMMMMNs`
                                 hs -sMy/      ./ymMMMMMMMMMMMMMMMMMMMMMNs.    `:sy
                                 `NNMMMMm`         ./sdMMMMMMMMMMMMMMMmo`   .+hNMMN
                                  hMMMMMMs          ods//odMMMMMMMNdo-   .odMMMMMMM
                                  `hMMMMMM+        sMMMMMdo:+oo+/-    .odMMMMMMMMMd
                                   `dMMMMMM:      sMMMMMMMMMmo.    .+dMMMMMMMMMMMm-
                                  -NMMMMMMMNso+/::+++syhdmMMMMNy.`hNMMMMMMMMMMMm+`
                                   /MMMMMMMMMMMMMMNNNmdhssMMMMMMN+:NMMMMMMMMNy:`
                                    /NMMMMMMMMMMMMMMMMMMMMMMMMMMMM//MMMMMNh/`
                                     .smMMMMMMMMMMMMMMMMMMMMMMMMMMN`dMNh+.
                                       `-dMMNddmNMMMMMMMMMMMMMMMMMM/:/.
                                         `...`so++sMMMMMMMMMMMMMMMMs
                                             .MMMNNMMMMMMMMMMMMMMMMs
                                             :MMMMMMMMMMMMMMMMMMMMM/
                                             /MMMMMMMMMMMMMMMMMMMMm`
                                             -MMMMMMMMMMMMMMMMMMMm:
                                              NMMMMMMMMMMMMMMNmdo.
                                              dMMMMMMMMmysso++o`
                                             `NMMMMMMMN.sdmmNMM.
                                             oMMMMMMMM//MMMMMMM.
                                            -NMMMMMMMh`NMMMMMMM.
                                            dMMMMMMMN..MMMMMMMM.
                                           /MMMMMMMM/ `MMMMMMMM`
                                           dMMMMMMMs   dMMMMMMN
                                           mMMMMMMd`   .hNMMMMd
                                           :NMMMMN.      .+yNMo
                                            -mMMN-           -`
                                             `oN:
                                               `

"""

                message = sendgrid.Message("ops@cloudcontrol.de", "You are operations hero", content.format(**data))
                message.add_to(["mw@cloudcontrol.de", person.email],
                               ["Matthias Wiesner", person.name])

                s.web.send(message)
                print "Notification was send to {hero}".format(**data)

            m = now + datetime.timedelta(days=1)
            t = datetime.datetime(m.year, m.month, m.day, 7, 0, 0)
            n = datetime.datetime.today()
            sleep(int((t - n).total_seconds()))
