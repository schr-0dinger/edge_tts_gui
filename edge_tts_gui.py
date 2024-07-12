import asyncio
import os, sys
import tkinter
from datetime import datetime
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import edge_tts
import requests
from PIL import ImageTk
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import threading
import webbrowser

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x440")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.title("EDGE TTS GUI")
        # Determine if running in a PyInstaller bundle
        if getattr(sys, 'frozen', False):
            # Running in a bundle
            base_path = sys._MEIPASS
        else:
            # Running in normal Python environment
            base_path = os.path.abspath(".")

        icon_path = os.path.join(base_path, "assets", "icon.ico")
        
        if not os.path.exists(icon_path):
            raise FileNotFoundError(f"Icon file not found: {icon_path}")

        self.iconpath = ImageTk.PhotoImage(file=icon_path)
        self.wm_iconbitmap(icon_path)
        self.iconphoto(False, self.iconpath)

        self.default_voice = "en-GB-RyanNeural"
        self.voice_names = ['af-ZA-AdriNeural', 'af-ZA-WillemNeural', 'am-ET-AmehaNeural', 'am-ET-MekdesNeural', 'ar-AE-FatimaNeural', 'ar-AE-HamdanNeural', 'ar-BH-AliNeural', 'ar-BH-LailaNeural', 'ar-DZ-AminaNeural', 'ar-DZ-IsmaelNeural', 'ar-EG-SalmaNeural', 'ar-EG-ShakirNeural', 'ar-IQ-BasselNeural', 'ar-IQ-RanaNeural', 'ar-JO-SanaNeural', 'ar-JO-TaimNeural', 'ar-KW-FahedNeural', 'ar-KW-NouraNeural', 'ar-LB-LaylaNeural', 'ar-LB-RamiNeural', 'ar-LY-ImanNeural', 'ar-LY-OmarNeural', 'ar-MA-JamalNeural', 'ar-MA-MounaNeural', 'ar-OM-AbdullahNeural', 'ar-OM-AyshaNeural', 'ar-QA-AmalNeural', 'ar-QA-MoazNeural', 'ar-SA-HamedNeural', 'ar-SA-ZariyahNeural', 'ar-SY-AmanyNeural', 'ar-SY-LaithNeural', 'ar-TN-HediNeural', 'ar-TN-ReemNeural', 'ar-YE-MaryamNeural', 'ar-YE-SalehNeural', 'az-AZ-BabekNeural', 'az-AZ-BanuNeural', 'bg-BG-BorislavNeural', 'bg-BG-KalinaNeural', 'bn-BD-NabanitaNeural', 'bn-BD-PradeepNeural', 'bn-IN-BashkarNeural', 'bn-IN-TanishaaNeural', 'bs-BA-GoranNeural', 'bs-BA-VesnaNeural', 'ca-ES-EnricNeural', 'ca-ES-JoanaNeural', 'cs-CZ-AntoninNeural', 'cs-CZ-VlastaNeural', 'cy-GB-AledNeural', 'cy-GB-NiaNeural', 'da-DK-ChristelNeural', 'da-DK-JeppeNeural', 'de-AT-IngridNeural', 'de-AT-JonasNeural', 'de-CH-JanNeural', 'de-CH-LeniNeural', 'de-DE-AmalaNeural', 'de-DE-ConradNeural', 'de-DE-FlorianMultilingualNeural', 'de-DE-KatjaNeural', 'de-DE-KillianNeural', 'de-DE-SeraphinaMultilingualNeural', 'el-GR-AthinaNeural', 'el-GR-NestorasNeural', 'en-AU-NatashaNeural', 'en-AU-WilliamNeural', 'en-CA-ClaraNeural', 'en-CA-LiamNeural', 'en-GB-LibbyNeural', 'en-GB-MaisieNeural', 'en-GB-RyanNeural', 'en-GB-SoniaNeural', 'en-GB-ThomasNeural', 'en-HK-SamNeural', 'en-HK-YanNeural', 'en-IE-ConnorNeural', 'en-IE-EmilyNeural', 'en-IN-NeerjaExpressiveNeural', 'en-IN-NeerjaNeural', 'en-IN-PrabhatNeural', 'en-KE-AsiliaNeural', 'en-KE-ChilembaNeural', 'en-NG-AbeoNeural', 'en-NG-EzinneNeural', 'en-NZ-MitchellNeural', 'en-NZ-MollyNeural', 'en-PH-JamesNeural', 'en-PH-RosaNeural', 'en-SG-LunaNeural', 'en-SG-WayneNeural', 'en-TZ-ElimuNeural', 'en-TZ-ImaniNeural', 'en-US-AnaNeural', 'en-US-AndrewMultilingualNeural', 'en-US-AndrewNeural', 'en-US-AriaNeural', 'en-US-AvaMultilingualNeural', 'en-US-AvaNeural', 'en-US-BrianMultilingualNeural', 'en-US-BrianNeural', 'en-US-ChristopherNeural', 'en-US-EmmaMultilingualNeural', 'en-US-EmmaNeural', 'en-US-EricNeural', 'en-US-GuyNeural', 'en-US-JennyNeural', 'en-US-MichelleNeural', 'en-US-RogerNeural', 'en-US-SteffanNeural', 'en-ZA-LeahNeural', 'en-ZA-LukeNeural', 'es-AR-ElenaNeural', 'es-AR-TomasNeural', 'es-BO-MarceloNeural', 'es-BO-SofiaNeural', 'es-CL-CatalinaNeural', 'es-CL-LorenzoNeural', 'es-CO-GonzaloNeural', 'es-CO-SalomeNeural', 'es-CR-JuanNeural', 'es-CR-MariaNeural', 'es-CU-BelkysNeural', 'es-CU-ManuelNeural', 'es-DO-EmilioNeural', 'es-DO-RamonaNeural', 'es-EC-AndreaNeural', 'es-EC-LuisNeural', 'es-ES-AlvaroNeural', 'es-ES-ElviraNeural', 'es-ES-XimenaNeural', 'es-GQ-JavierNeural', 'es-GQ-TeresaNeural', 'es-GT-AndresNeural', 'es-GT-MartaNeural', 'es-HN-CarlosNeural', 'es-HN-KarlaNeural', 'es-MX-DaliaNeural', 'es-MX-JorgeNeural', 'es-NI-FedericoNeural', 'es-NI-YolandaNeural', 'es-PA-MargaritaNeural', 'es-PA-RobertoNeural', 'es-PE-AlexNeural', 'es-PE-CamilaNeural', 'es-PR-KarinaNeural', 'es-PR-VictorNeural', 'es-PY-MarioNeural', 'es-PY-TaniaNeural', 'es-SV-LorenaNeural', 'es-SV-RodrigoNeural', 'es-US-AlonsoNeural', 'es-US-PalomaNeural', 'es-UY-MateoNeural', 'es-UY-ValentinaNeural', 'es-VE-PaolaNeural', 'es-VE-SebastianNeural', 'et-EE-AnuNeural', 'et-EE-KertNeural', 'fa-IR-DilaraNeural', 'fa-IR-FaridNeural', 'fi-FI-HarriNeural', 'fi-FI-NooraNeural', 'fil-PH-AngeloNeural', 'fil-PH-BlessicaNeural', 'fr-BE-CharlineNeural', 'fr-BE-GerardNeural', 'fr-CA-AntoineNeural', 'fr-CA-JeanNeural', 'fr-CA-SylvieNeural', 'fr-CA-ThierryNeural', 'fr-CH-ArianeNeural', 'fr-CH-FabriceNeural', 'fr-FR-DeniseNeural', 'fr-FR-EloiseNeural', 'fr-FR-HenriNeural', 'fr-FR-RemyMultilingualNeural', 'fr-FR-VivienneMultilingualNeural', 'ga-IE-ColmNeural', 'ga-IE-OrlaNeural', 'gl-ES-RoiNeural', 'gl-ES-SabelaNeural', 'gu-IN-DhwaniNeural', 'gu-IN-NiranjanNeural', 'he-IL-AvriNeural', 'he-IL-HilaNeural', 'hi-IN-MadhurNeural', 'hi-IN-SwaraNeural', 'hr-HR-GabrijelaNeural', 'hr-HR-SreckoNeural', 'hu-HU-NoemiNeural', 'hu-HU-TamasNeural', 'id-ID-ArdiNeural', 'id-ID-GadisNeural', 'is-IS-GudrunNeural', 'is-IS-GunnarNeural', 'it-IT-DiegoNeural', 'it-IT-ElsaNeural', 'it-IT-GiuseppeNeural', 'it-IT-IsabellaNeural', 'ja-JP-KeitaNeural', 'ja-JP-NanamiNeural', 'jv-ID-DimasNeural', 'jv-ID-SitiNeural', 'ka-GE-EkaNeural', 'ka-GE-GiorgiNeural', 'kk-KZ-AigulNeural', 'kk-KZ-DauletNeural', 'km-KH-PisethNeural', 'km-KH-SreymomNeural', 'kn-IN-GaganNeural', 'kn-IN-SapnaNeural', 'ko-KR-HyunsuNeural', 'ko-KR-InJoonNeural', 'ko-KR-SunHiNeural', 'lo-LA-ChanthavongNeural', 'lo-LA-KeomanyNeural', 'lt-LT-LeonasNeural', 'lt-LT-OnaNeural', 'lv-LV-EveritaNeural', 'lv-LV-NilsNeural', 'mk-MK-AleksandarNeural', 'mk-MK-MarijaNeural', 'ml-IN-MidhunNeural', 'ml-IN-SobhanaNeural', 'mn-MN-BataaNeural', 'mn-MN-YesuiNeural', 'mr-IN-AarohiNeural', 'mr-IN-ManoharNeural', 'ms-MY-OsmanNeural', 'ms-MY-YasminNeural', 'mt-MT-GraceNeural', 'mt-MT-JosephNeural', 'my-MM-NilarNeural', 'my-MM-ThihaNeural', 'nb-NO-FinnNeural', 'nb-NO-PernilleNeural', 'ne-NP-HemkalaNeural', 'ne-NP-SagarNeural', 'nl-BE-ArnaudNeural', 'nl-BE-DenaNeural', 'nl-NL-ColetteNeural', 'nl-NL-FennaNeural', 'nl-NL-MaartenNeural', 'pl-PL-MarekNeural', 'pl-PL-ZofiaNeural', 'ps-AF-GulNawazNeural', 'ps-AF-LatifaNeural', 'pt-BR-AntonioNeural', 'pt-BR-FranciscaNeural', 'pt-BR-ThalitaNeural', 'pt-PT-DuarteNeural', 'pt-PT-RaquelNeural', 'ro-RO-AlinaNeural', 'ro-RO-EmilNeural', 'ru-RU-DmitryNeural', 'ru-RU-SvetlanaNeural', 'si-LK-SameeraNeural', 'si-LK-ThiliniNeural', 'sk-SK-LukasNeural', 'sk-SK-ViktoriaNeural', 'sl-SI-PetraNeural', 'sl-SI-RokNeural', 'so-SO-MuuseNeural', 'so-SO-UbaxNeural', 'sq-AL-AnilaNeural', 'sq-AL-IlirNeural', 'sr-RS-NicholasNeural', 'sr-RS-SophieNeural', 'su-ID-JajangNeural', 'su-ID-TutiNeural', 'sv-SE-MattiasNeural', 'sv-SE-SofieNeural', 'sw-KE-RafikiNeural', 'sw-KE-ZuriNeural', 'sw-TZ-DaudiNeural', 'sw-TZ-RehemaNeural', 'ta-IN-PallaviNeural', 'ta-IN-ValluvarNeural', 'ta-LK-KumarNeural', 'ta-LK-SaranyaNeural', 'ta-MY-KaniNeural', 'ta-MY-SuryaNeural', 'ta-SG-AnbuNeural', 'ta-SG-VenbaNeural', 'te-IN-MohanNeural', 'te-IN-ShrutiNeural', 'th-TH-NiwatNeural', 'th-TH-PremwadeeNeural', 'tr-TR-AhmetNeural', 'tr-TR-EmelNeural', 'uk-UA-OstapNeural', 'uk-UA-PolinaNeural', 'ur-IN-GulNeural', 'ur-IN-SalmanNeural', 'ur-PK-AsadNeural', 'ur-PK-UzmaNeural', 'uz-UZ-MadinaNeural', 'uz-UZ-SardorNeural', 'vi-VN-HoaiMyNeural', 'vi-VN-NamMinhNeural', 'zh-CN-XiaoxiaoNeural', 'zh-CN-XiaoyiNeural', 'zh-CN-YunjianNeural', 'zh-CN-YunxiNeural', 'zh-CN-YunxiaNeural', 'zh-CN-YunyangNeural', 'zh-CN-liaoning-XiaobeiNeural', 'zh-CN-shaanxi-XiaoniNeural', 'zh-HK-HiuGaaiNeural', 'zh-HK-HiuMaanNeural', 'zh-HK-WanLungNeural', 'zh-TW-HsiaoChenNeural', 'zh-TW-HsiaoYuNeural', 'zh-TW-YunJheNeural', 'zu-ZA-ThandoNeural', 'zu-ZA-ThembaNeural']
        self.radio_var = tkinter.IntVar(value=1)

        self.check_internet_conn()
        self.create_widgets()

    def check_internet_conn(self):
        try:
            response = requests.get('https://www.google.com', timeout=3)
            if response.status_code != 200:
                self.show_warning("Unable to connect!")
        except requests.RequestException:
            self.show_warning("Unable to connect!")
            exit()

    def show_warning(self, message):
        msg = CTkMessagebox(title="Warning Message!", message=message, icon="warning", option_1="Cancel", option_2="Retry")
        if msg.get() == "Retry":
            self.check_internet_conn()
        else:
            self.exit_app()

    def show_info(self):
        about = CTkMessagebox(title="About", message="𝙀𝘿𝙂𝙀 𝙏𝙏𝙎 𝙂𝙐𝙄\nversion:0.1-alpha\n𝘽𝙮 𝙨𝙘𝙝𝙧_𝙤𝙙𝙞𝙣𝙜𝙚𝙧", icon="info", option_1="OK", option_2="Github")
        response = about.get()

        if response == "Github":
            url = "https://github.com/schr-0dinger/edge_tts_gui"
            webbrowser.open(url, new=0, autoraise=True)

    def show_empty(self):
        CTkMessagebox(title="Warning Message!", message="Text box cannot be empty", icon="warning", option_1="OK")
        self.btn_preview.configure(state="normal")  

    async def convert(self, TEXT, VOICE, OUTPUT_FILE, RATE, PITCH, VOLUME):
        communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, pitch=PITCH, volume=VOLUME)
        await communicate.save(OUTPUT_FILE)

    async def preview(self, TEXT, VOICE, OUTPUT_FILE, RATE, PITCH, VOLUME):
        communicate = edge_tts.Communicate(TEXT, VOICE, rate=RATE, pitch=PITCH, volume=VOLUME)
        with open(OUTPUT_FILE, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])

    def play_audio(self, file_path, playback_event):
        audio = AudioSegment.from_file(file_path)
        self.change_preview_button_text("PLAYING", "GREEN")
        play(audio)
        self.change_preview_button_text("PREVIEW", "#41436A")
        self.btn_preview.configure(state="normal")
        playback_event.set()

    def change_preview_button_text(self, text, color):
        self.btn_preview.configure(text=text, fg_color=color)

    def on_convert(self):
        TEXT = self.ent.get("1.0", "end-1c")
        VOICE = self.combox.get()
        RATE, PITCH, VOLUME = self.get_audio_properties()
        OUTPUT_FILE = self.get_output_filename(TEXT, VOICE)
        if len(TEXT) != 0 :
            if isinstance(OUTPUT_FILE, str):
                asyncio.run(self.convert(TEXT, VOICE, OUTPUT_FILE, RATE, PITCH, VOLUME))
        else:    
            self.show_empty()    

    def on_preview(self):
        TEXT = self.ent.get("1.0", "end-1c")
        VOICE = self.combox.get()
        RATE, PITCH, VOLUME = self.get_audio_properties()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            OUTPUT_FILE = temp_file.name
            if len(TEXT) != 0:    
                asyncio.run(self.preview(TEXT, VOICE, OUTPUT_FILE, RATE, PITCH, VOLUME))
                playback_event = threading.Event()
                threading.Thread(target=self.play_audio, args=(OUTPUT_FILE, playback_event)).start()
                playback_event.wait()
                os.remove(OUTPUT_FILE)
            else:    
                self.show_empty()   

    def start_convert_thread(self):
        threading.Thread(target=self.on_convert).start()

    def start_preview_thread(self):
        self.btn_preview.configure(state="disabled", text="PROCESSING")
        threading.Thread(target=self.on_preview).start()

    def get_audio_properties(self):
        RATE = f"{'+' if int(self.rate_scale.get()) >= 0 else ''}{int(self.rate_scale.get())}%"
        PITCH = f"{'+' if int(self.pitch_scale.get()) >= 0 else ''}{int(self.pitch_scale.get())}Hz"
        VOLUME = f"{'+' if int(self.vol_scale.get()) >= 0 else ''}{int(self.vol_scale.get())}%"
        return RATE, PITCH, VOLUME

    def get_output_filename(self, TEXT, VOICE):
        now_str = datetime.now().strftime("%B %d %Y %H-%M-%S")
        if self.radio_var.get() == 1:
            return f"{VOICE}{now_str}.mp3"
        elif self.radio_var.get() == 2:
            return f"{TEXT[:11].replace(' ', '_')}.mp3"
        else:
            return ctk.CTkInputDialog(text="Enter Output file name", title="Save As").get_input() + ".mp3"

    def update_scales(self, event=None):
        self.rate_scale_lbl.configure(text="RATE " + str(int(self.rate_scale.get())))
        self.pitch_scale_lbl.configure(text="PITCH " + str(int(self.pitch_scale.get())))
        self.vol_scale_lbl.configure(text="VOLUME " + str(int(self.vol_scale.get())))

    def reset_scales(self):
        self.rate_scale.set(0)
        self.pitch_scale.set(0)
        self.vol_scale.set(0)
        self.update_scales() 

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="EDGE TTS GUI", font=("Helvetica", 24, "bold"), corner_radius=10)
        self.label.place(x=120, y=10)
        self.combox = ctk.CTkComboBox(self, values=self.voice_names, width=260, hover=True)
        self.combox.set(self.default_voice)
        self.combox.place(x=60, y=50)
        self.ent = ctk.CTkTextbox(self, width=300, height=300, border_color="#41436A", border_width=1)
        self.ent.place(x=40, y=90)
        self.create_scale_frame()
        self.btn = ctk.CTkButton(self, text="GENERATE", command=self.start_convert_thread, width=100, height=50, fg_color="#F64668")
        self.btn.place(x=400, y=250)
        self.btn_preview = ctk.CTkButton(self, text="PREVIEW", command=self.start_preview_thread, width=100, height=50, fg_color="#41436A")
        self.btn_preview.place(x=400, y=310)
        self.create_rename_frame()
        self.reset_scale_btn = ctk.CTkButton(self, text="RESET", command=self.reset_scales, width=10)
        self.reset_scale_btn.place(x=640, y=30)
        self.info = ctk.CTkButton(self, text="About", width=100, command=self.show_info)
        self.info.place(x=650, y=400)

    def create_scale_frame(self):
        self.scale_frame = ctk.CTkFrame(self, border_color="#41436A", border_width=1)
        self.scale_frame.place(x=400, y=20)
        self.rate_scale = ctk.CTkSlider(self.scale_frame, from_=-100, to=100, width=300)
        self.rate_scale.grid(column=0, row=1, pady=10, padx=6, sticky='nsw')
        self.pitch_scale = ctk.CTkSlider(self.scale_frame, from_=-100, to=100, width=300)
        self.pitch_scale.grid(column=0, row=3, pady=10, padx=6, sticky='nsw')
        self.vol_scale = ctk.CTkSlider(self.scale_frame, from_=-100, to=100, width=300)
        self.vol_scale.grid(column=0, row=5, pady=10, padx=6, sticky='nsw')
        self.rate_scale_lbl = ctk.CTkLabel(self.scale_frame, text="RATE " + str(int(self.rate_scale.get())))
        self.rate_scale_lbl.grid(column=0, row=0, pady=4)
        self.pitch_scale_lbl = ctk.CTkLabel(self.scale_frame, text="PITCH " + str(int(self.pitch_scale.get())))
        self.pitch_scale_lbl.grid(column=0, row=2)
        self.vol_scale_lbl = ctk.CTkLabel(self.scale_frame, text="VOLUME " + str(int(self.vol_scale.get())))
        self.vol_scale_lbl.grid(column=0, row=4)
        for scale in [self.rate_scale, self.pitch_scale, self.vol_scale]:
            scale.bind("<Motion>", self.update_scales)
            scale.bind("<ButtonRelease-1>", self.update_scales)

    def create_rename_frame(self):
        self.rename_frame = ctk.CTkFrame(self)
        self.rename_frame.place(x=560, y=250)
        self.rename_label = ctk.CTkLabel(self.rename_frame, text="Save As options:", font=("Helvetica", 12, "bold"))
        self.rename_label.grid(column=0, row=0, padx=6, pady=2, sticky='w')
        for idx, text in enumerate(["Voice + Timestamp", "First 10 chars of text entered", "Enter manual name"], start=1):
            ctk.CTkRadioButton(self.rename_frame, text=text, variable=self.radio_var, value=idx).grid(column=0, row=idx, padx=6, pady=2, sticky='w')

if __name__ == "__main__":
    app = App()
    app.mainloop()


