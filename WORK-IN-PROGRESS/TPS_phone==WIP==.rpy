# THESE FUNCTIONS ARE USED IN THE TPS' "PHONE SUITE"

############################################################################################################################
#
# EXTRA: this function simulates cancelling of a message - will become part of the rhythmic_say one day...
#
############################################################################################################################
init python:
    import random

    def erase_and_rewind(who, text, font="fonts/OpenSans-Medium.ttf", hold=1.4):

        L = len(text)

        # punto di esitazione
        slow_start = int(L * random.uniform(0.60, 0.85))

        # se deve riaccelerare
        reaccel_point = int(L * 0.10)

        current = L

        # mostra il messaggio completo
        renpy.say(who, generate_tapped_text(text,font) + "{w=" + str(hold) + "}{nw}")

        while current > 0:

            # quanti caratteri cancella
            step = random.randint(1, 4)

            current = max(0, current - step)

            partial = text[:current]

            # velocità base
            wait = random.uniform(0.08, 0.12)

            # zona di rallentamento
            if current < slow_start and current > reaccel_point:
                wait *= random.uniform(1.6, 2.4)

            # riaccelerazione finale
            if current <= reaccel_point:
                wait *= random.uniform(0.5, 0.8)

            renpy.say(
                who,
                "{font=" + font + "}" + partial + "{/font}{fast}{w=" + str(wait) + "}{nw}"
            )

    def generate_tapped_text(text, font="fonts/OpenSans-Medium.ttf"):

        tapping_speed = random.randint(35,45)

        tapped = []
        tapped.append("{font=" + font + "}{cps=" + str(tapping_speed) + "}")

        for ch in text:

            # 70% continua con stessa velocità
            if random.random() < 0.7:
                tapped.append(ch)

            else:
                # cambia velocità
                if 35 <= tapping_speed <= 45:
                    tapping_speed = random.choice([
                        random.randint(20,30),
                        random.randint(50,60)
                    ])

                elif 20 <= tapping_speed <= 30:
                    tapping_speed = random.randint(30,45)

                else:
                    tapping_speed = random.randint(35,60)

                tapped.append("{/cps}{cps=" + str(tapping_speed) + "}" + ch)

        tapped.append("{/cps}{/font}")

        return "".join(tapped)