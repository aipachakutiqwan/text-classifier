"""
Text Preprocessing class
"""
import re
import unicodedata
import nltk
from src.utils.stopwords import UNIGRAM_STOPWORDS, BIGRAM_STOPWORDS, TRIGRAM_STOPWORDS
from src.utils.cleaner_regex import WEB_TOKENS, \
    SIGNATURE_REGEXES, GREETING_REGEXES, NORMALIZATION_REGEXES


def read_stopwords(n_words):
    """
    Assign N-gram according to number words
    :param n_words:
    :return:
    """
    return TRIGRAM_STOPWORDS if n_words == 3 \
        else BIGRAM_STOPWORDS if n_words == 2 \
        else UNIGRAM_STOPWORDS if n_words == 1 \
        else []


class Preprocessing:
    """
    Cleaner class
    """
    unigram_stopwords = read_stopwords(n_words=1)
    bigram_stopwords = read_stopwords(n_words=2)
    trigram_stopwords = read_stopwords(n_words=3)

    @classmethod
    def clean(cls, text):
        """
        Clean steps
        :param text:
        :return:
        """
        clean_text = str(text).lower()
        content_stripped = cls.strip_content(clean_text, chunks=[])
        clean_text = cls.remove_signatures(content_stripped)
        #clean_text = cls.remove_html(clean_text)
        clean_text = cls.normalize_words(clean_text)
        clean_text = cls.unidecode_text(clean_text)
        clean_text = cls.remove_symbols(clean_text)
        clean_text = cls.normalize_words(clean_text)
        clean_text = cls.remove_unitokens(clean_text)
        clean_text = cls.remove_stopwords(clean_text)
        clean_text = cls.normalize_words(clean_text)
        return clean_text

    @classmethod
    def remove_html(cls, text):
        """
        Remove html from text
        :param text:
        :return:
        """
        list_text = text.split()
        for web_token in WEB_TOKENS:
            for token in text.split():
                if web_token in token:
                    try:
                        list_text.remove(token)
                    except Exception as excep:
                        print(f"Exception in remove_html {excep}")
                        pass
        return " ".join(list_text)

    @classmethod
    def remove_unitokens(cls, text):
        """
        Remove unitokens
        :param text:
        :return:
        """
        text = re.sub(r"(\b\w\b)", " ", text)
        return " ".join(text.split())

    @classmethod
    def unidecode_text(cls, text):
        """
        Unidecode text
        :param text:
        :return:
        """
        text = unicodedata.normalize("NFKD", text)
        text = u"".join([character for character in text if not unicodedata.combining(character)])
        return " ".join(text.split())

    @classmethod
    def remove_stopwords(cls, text):
        """
        Remove stop words
        :param text:
        :return:
        """
        trigrams = list(nltk.ngrams(text.split(), 3))
        found_trigram_stopwords = [stopword for trigram in trigrams
                                   for stopword in cls.trigram_stopwords
                                   if " ".join(trigram) == stopword]
        for stopword in found_trigram_stopwords:
            text = text.replace(stopword, " ")

        bigrams = list(nltk.ngrams(text.split(), 2))
        found_bigram_stopwords = [stopword for bigram in bigrams
                                  for stopword in cls.bigram_stopwords
                                  if " ".join(bigram) == stopword]
        for stopword in found_bigram_stopwords:
            text = text.replace(stopword, " ")

        found_unigram_stopwords = [w for w in cls.unigram_stopwords if w in text.split()]
        clean_text = [w for w in text.split() if w not in found_unigram_stopwords]
        return " ".join(clean_text)

    @classmethod
    def remove_symbols(cls, text):
        """
        Remove symbols
        :param text:
        :return:
        """
        f23 = False
        f24 = False
        for token in text.split():
            if "f23" in token:
                f23 = True
                break
        for token in text.split():
            if "f24" in token:
                f24 = True
                break
        regex = re.compile("[^a-zA-Z ]")
        clean_text = " ".join(s for s in text.split()
                              if not any(c.isdigit() for c in s))
        clean_text = regex.sub(" ", clean_text)
        if f23:
            clean_text = f"f23 {clean_text}"
        if f24:
            clean_text = f"f24 {clean_text}"
        return " ".join(clean_text.split())

    @classmethod
    def normalize_words(cls, text):
        """
        Normalize words
        :param text:
        :return:
        """
        for regex, token in NORMALIZATION_REGEXES.items():
            if re.findall(regex, text):
                text = re.sub(regex, token, text)
        return text

    @classmethod
    def cut_greetings(cls, text):
        """
        delete greetings from text
        :param text:
        :return:
        """
        for hook in GREETING_REGEXES:
            if re.findall(hook, text):
                token = re.findall(hook, text)[0]
                idx = text.index(token)
                check_text = text[:idx]
                if len(check_text.split()) <= 5:
                    continue
                else:
                    text = text[:idx]
        return text.strip()

    @classmethod
    def cut_signature(cls, text):
        """
        Cut signatures from the text
        :param text:
        :return:
        """
        for regex in SIGNATURE_REGEXES:
            if re.findall(regex, text):
                token = re.findall(regex, text)[0]
                idx = text.index(token)
                text = text[:idx]
        return text.strip()

    @classmethod
    def remove_signatures(cls, bodies):
        """
        Remove signatures
        :param bodies:
        :return:
        """
        bodies = [cls.cut_greetings(body) for body in bodies]
        return cls.cut_signature(bodies[0])

    @classmethod
    def strip_content(cls, text, chunks):
        """
        Remove whitespaces from the start and the end of the string.
        :param text:
        :param chunks:
        :return:
        """
        chunks.append(text.strip())
        return chunks
    


if __name__ == "__main__":
    
    text = "ESMIAS,POSTBOKS438,1471LØRENSKOGTEL.:48222200FAX.:67917610 BRUKSANVISNINGFORESABRANNALARMSENTRAL BRANN                                       ESA BRANN                                  FLEREALARMER               FORVARSELSLOKKEANLEGGAKTIVERT              FEIL                                                 STOPP/STARTALARM               BRANNVENTILASJONAKTIVERT                  SYSTEMFEIL               ALARMOVERFØRINGAKTIVERT                   SERVICE                                                 TILBAKESTILL ALARMOVERFØRING                                                          KLOKKEKURS               TILBAKESTILLINGMISLYKKET                                                           FRAKOBLING               SONER IBRANNALARM               1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16                                          IDRIFT TEST    FORSINKETALARM               17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32                                          FRA-KOBLE TIL-KOBLE ALARMKLOKKERSTOPPET                                                   TEST                                                         BATTERIDRIFT                                                         DAGSTILLINGNØKKELSAFEÅPEN                                     VALG                                                         AKTIVERINGAVAL.KLOKKER                                                                    66521160GB Innhold:Side Informasjonvedinstallasjon               2              Brannalarm/kvitteringogtilbakestilling   3              Utkoblingavadressersomikkegårtilbaketilnormaltilstand 3 Feilalarm /Servicealarm                  4              Utkobling /innkobling                    5              Tester                                    6              Menydiagram                               7 NB!                  Lesgrundiggjennombruksanvisningenførbrannalarmsentralentas ibruk.                  Oppbevarbruksanvisningen itilknytningtilsentralen. 01501158/NO55A ESAbrannvarslingsystem,brukerinformasjon (Fyllesutavdenansvarligeforbrannvarslingssystemetnårsystemettas ibruk) Eier/innehaveravlokalene Lokalenesnavn Lokalenesadresse Ansvarligforbrannvarslingssystemet Telefon Eventuellstedfortrederfordenansvarlige Telefon Detektorsløyfenr./antalladresser            1)_____________________2)______________________3)__________________4)___________________ 2 BRANNALARM      /                                                              Kunforansvarshavende!             kvitteringogtilbakestilling Slåavalarmlydenved åtrykke                                                          STOPP/STARTALARM                 påSTOPP/STARTALARM-Knappen.                                                KLIKK Blagjennomalarmmeldingene.        FLEREALARMER KLIKK,KLIKK... HoldinneTILBAKESTILL-Knappensålengelydsignalethøres.Systemetsettesderetter                                                          TILBAKESTILL i                 normatilstand,                                                    KLIIIIIKK BRANNALARMR:030:01.17001/003 ESA               BRANN                                   BRANN                                 FLEREALARMER              FORVARSELSLOKKEANLEGGAKTIVERT           FEIL                                              STOPP/STARTALARM              BRANNVENTILASJONAKTIVER                SYSTEMFEIL              ALARMOVERFØRINGAKTIVERT                 SERVICE                                              TILBAKESTILL ALARMOVERFØRING              TILBAKESTILLINGMISLYKKET                 KLOKKEKURS                                                       FRAKOBLING              SONER IBRANNALARM              1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16                                     IDRIFT   TEST    FORSINKETALARM              17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32                                        FRAKOBLE TIL-KOBLE ALARMKLOKKERSTOPPET                                                TEST                                                      BATTERIDRIFT                                   VELG              DAGSTILLINGNØKKELSAFEÅPENAKTIVERINGAVAL.KLOKKER                                                                66521160GB             Frakoblingavadressersomikkegårtilbaketilnormaltilstand:                                                          FRA-KOBLE TIL-KOBLE TEST           Nåradressenvises idisplayet,trykk                                                    VELG           Frakoblingsknapp.                                           3 FEILALARM      /Servicealarm SlåavalarmlydenvedåtrykkepåSTOPP/STARTALARM-knappen                                                       STOPP/STARTALARM FLEREALARMER                 Blagjennomalarmmeldingene HoldinneTILBAKESTILLINGS-knappensålengelydsignalethøres.Systemetsettesderetterinormaltilstand TILBAKESTILL BRANNALARMR:030:01.17001/003 ESA               BRANN                                   BRANN                                 FLEREALARMER              FORVARSELSLOKKEANLEGGAKTIVERT           FEIL                                              STOPP/STARTALARMS              BRANNVENTILASJONAKTIVERT               SYSTEMFEIL              ALARMOVERFØRINGAKTIVERT                 SERVICE                                              TILBAKETILL ALARMOVERFØRING              TILBAKESTILLINGMISLYKKET                 KLOKKEKURS                                                       FRAKOBLING              SONER IBRANNALARM              1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16                                     IDRIFT   TEST    FORSINKETALARM              17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32                                        FRA.KOBLE TIL-KOBLE TEST ALARMKLOKKERSTOPPET                                                      BATTERIDRIFTDAGSTILLINGNØKKELSAFEÅPENAKTIV                                   VELG                                                                66521160GB           Frakoblingavadresserellerfeiloverføring                                                            NB!             Koblefranårdenaktuellefeil-ellerservicealarmvisespådisplayet.Merkatfrakoblingikkeermuligiallesituasjoner.                                               FRA-KOBLE TIL-KOBLE                                                        TEST   KONTAKTALLTIDESMISERVICEITILFELLEFEIL.                                          VELG 4 Huskatfrakoblingerkanforhindrealarm.            FRAKOBLING       /Tilkobling                                                       NB! Velgfunksjon GåtilønsketstedpåmenyenvedhjelpavVELG-knappen.(Sefullstendigmenydiagramside7) VELG Menydiagram                Tilkobling/frakobling          FRA-KOBLE TIL-KOBLE                                                         TEST                                                                ALARMOVERFØRINGSTEST                Kobletilellerfraønsketfunksjon.(Soner,sløyfer,adresser,kontroller,feilovervåkning) VELG                                                                SYSTEMTEST                                                                TID Nårenfunksjonerblittfrakoblet,lysersignallampenforfrakobling.. FEIL                                                                BRUKERNIVÅ                                           SYSTEMFEIL                                           SERVICE                                                                UTSKRIFTER                                            ALARMOVERFØRING                                            KLOKKEKURS                                            FRAKOBLING                                                                HENDELSESLOGG           Blagjennomfrakoblingssregisteretogkoble              AKTIVEFRAKOBLINGERAKTIVEFEILAKTIVFORVARSEL VELG VELG                                                 VELG                                                                OVERVÅKNINGER STYRINGER Fra-koble Til-koble                                     TEST                       SLØYFE/ADRESSE                     VELG                                                                SONE /ADRESSE 5 TESTER Velgfunksjon GåtilønsketstedpåmenyenvedhjelpavVELG-knappen(sefullstendigmenydiagramside.7) VELG IDRIFT TEST Starttest                     FRA-KOBLE TIL-KOBLE TEST VELG IDRIFT TEST                Avslutttest                                              FRA-KOBLE TIL-KOBLE                                                       TEST                                                                Menydiagram                                         VELG                                                                Alarmoverføringstest                                                                SYSTEMTEST                Månedligtest /                alarmoverføringstest                            TID                                                IDRIFT TEST                Alarmøverføringstest:Huskåvarslealarmstasjonen/vaktsentralen.Kontrolleratmeldingenblemottattettertesten.                                              FRA-KOBLE TIL-KOBLE BRUKERNIVÅ                                                        TEST                                         VELG                   UTSKRIFTER                                                                HENDELSESLOGG                                                                AKTIVEFRAKOBLINGERAKTIVEFEILAKTIVFORVARSEL                Displaytest                                              FRA-KOBLE TIL-KOBLE TEST                Trykkinndørknappenogholdedeninnei10sekunder.TrykkengangpåTEST-knappen                                         VELG                                                                     VELG                Testingavstyringerogovervåkninger                                             POWERSUPPLY TEST                                              FRA-KOBLE TIL-KOBLE                                                        TEST                                                                OVERVÅKNINGER                                         VELG                Velgstyringellerovervåkning,ogtrykkpåTEST-knappen.Lukkderetterdørenvedstyringstest.Nårduvilavsluttestyringstesten,åpnerdudørenogsentralengårtilbaketilnormaltilstand(alletester,bortsettfradisplaytest,avsluttesvedåtrykkepåTILKOBLE-knappen).                                                                STYRINGER                                                                SLØYFE/ADRESSE SONE/ADRESSE 6 ALARMOVERFØRINGSTEST E T Menydiagram E T          SYSTEMTEST                                            KnappeneFRAKOBLE,TILKOBLEogTESTermarkermedfargeridennebruksanvisningen.EtminiatyrsymbolIsammefargebetyratfunksjonenkanbrukespådettepunktet.                                      E                           FRAKOBLE          TID            INNSTILLTID/DATO                         BYTTTILBRUKERNIVÅ 3 E          BRUKERNIVÅL                                                                   TILKOBLE                                     D E                         STARTSTATUSUTSRIFT                                     D E                         STARTFRAKOBINGSUTSKRIFT                   TEST                                     D E          UTSKRIFTER     STARTHENDELSESUTSKRIFT                                                    E                         SLETTHENDELSESREGISTER SLETT                                        SISTEHENDELSE          HENDELSESLOGG  SLETT          FØRSTEHENDELSE          AKTIVEFRAKOBLINGERAKTIVEFEILMELDINGERAKTIVEFORVARSEL            E                                                              SISTEFRAKOBLING                                                                          E                                              AKTIVEFRAKOBLINGER FØRSTEFRAKOBLING                    MedVELG-pilenekanduorienteredegidiagrammet SISTEFEIL                                   I                                              AKTIVEFEIL      FØRSTEFEIL                    denretningpileneviser.                                                              SISTEFORVARSEL                       DukanaktiveremenydiagrammetvedåtrykkeentenvenstreellerhøyreVELG-pil.                                              AKTIVEFORVARSEL FØRSTEFORVARSEL                VELG                                         D E T                         SIKRINGOVERVÅKNING           Frakobling,feilalarmogforvarselregisteretsynesbareomdetfinneshendelseridisseregistrene.                                         D E T                         JORDFEILOVERVÅKNING                                         D E T                         STRØMFORSYNINGOVERVÅKNING                                         D E T                         SLOKKEANLEGGOVERVÅKNING                                         D E T                         ALARMORGANEROVERVÅKNING                                         D E T                         FEILOVERFØRINGOVERVÅKNING                                         D E T          OVERVÅKNINGER  ALARMOVERFØRINGOVERVÅKNING                                         D E T                         ALARMUTGANGERUTSTYRNING                         SLOKKEANLEGGSTYRNING                         ALARMORGANSTYRNING                         FEILOVERFØRINGSTYRNING                                            T          STYRINGER      ALARMOVERFØRINGSTYRNING                                       SISTEADRESSE ISLØYFE D E INFOOMSISTEADRESSE/DETEKTORTYPEISLØYFE D E                         DETEKTORSLØYFE 2          SLØYFE/ADRESSE DETEKTORSLØYFE 1 FØRSTEADRESSE ISLØYFE D E INFOOMFØRSTEADRESSE/DETEKTORTYPEISLØYFE D E                                    D E             D E                D E                                       SISTEADRESSE ISONE INFOOMSISTEADRESSE/DETEKTORTYPEISONE                         SONE32                                    D E FØRSTEADRESSE ISONE D E INFOOMFØRSTEADRESSE/DETEKTORTYPEISONE D E          SONE/ADRESSE   SONE01                                           7"
    clean_text = Preprocessing().clean(text=text)
    print(clean_text)