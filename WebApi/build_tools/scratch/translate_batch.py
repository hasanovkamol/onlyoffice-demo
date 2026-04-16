import json
import os

def update_locale(uz_path, en_path, mapping):
    if not os.path.exists(uz_path) or not os.path.exists(en_path):
        return

    with open(en_path, 'r', encoding='utf-8') as f:
        en_data = json.load(f)
    with open(uz_path, 'r', encoding='utf-8') as f:
        uz_data = json.load(f)

    def translate_recursive(uz_obj, en_obj, path=""):
        if isinstance(uz_obj, dict):
            for k, v in en_obj.items():
                current_path = f"{path}.{k}" if path else k
                
                if k not in uz_obj:
                    uz_obj[k] = v # Add missing key from English
                
                if isinstance(v, dict):
                    if not isinstance(uz_obj.get(k), dict):
                        uz_obj[k] = {}
                    translate_recursive(uz_obj[k], v, current_path)
                else:
                    # Priority 1: Exact path match in mapping
                    if current_path in mapping:
                        uz_obj[k] = mapping[current_path]
                    # Priority 2: Common terms based on English value
                    else:
                        val = str(v)
                        # Only translate if it's currently English or empty
                        if uz_obj[k] == v or not uz_obj[k]:
                            low_val = val.lower().strip()
                            if low_val == "save": uz_obj[k] = "Saqlash"
                            elif low_val == "close": uz_obj[k] = "Yopish"
                            elif low_val == "cancel": uz_obj[k] = "Bekor qilish"
                            elif low_val == "ok": uz_obj[k] = "OK"
                            elif low_val == "yes": uz_obj[k] = "Ha"
                            elif low_val == "no": uz_obj[k] = "Yo'q"
                            elif low_val == "about": uz_obj[k] = "Haqida"
                            elif low_val == "version": uz_obj[k] = "Versiya"
                            elif low_val == "address": uz_obj[k] = "Manzil"
                            elif low_val == "back": uz_obj[k] = "Orqaga"
                            elif low_val == "edit": uz_obj[k] = "Tahrirlash"
                            elif low_val == "delete": uz_obj[k] = "O'chirish"
                            elif low_val == "loading...": uz_obj[k] = "Yuklanmoqda..."
                            elif low_val == "warning": uz_obj[k] = "Ogohlantirish"
                            elif low_val == "error": uz_obj[k] = "Xato"
                            elif low_val == "settings": uz_obj[k] = "Sozlamalar"
                            elif low_val == "help": uz_obj[k] = "Yordam"
                            elif low_val == "search": uz_obj[k] = "Qidiruv"
                            elif low_val == "find": uz_obj[k] = "Topish"
                            elif low_val == "apply": uz_obj[k] = "Qo'llash"
                            elif low_val == "done": uz_obj[k] = "Tayyor"
                            elif low_val == "print": uz_obj[k] = "Chop etish"
                            elif low_val == "download": uz_obj[k] = "Yuklab olish"
                            elif low_val == "share": uz_obj[k] = "Ulashish"
                            elif low_val == "theme": uz_obj[k] = "Mavzu"
                            elif low_val == "dark": uz_obj[k] = "To'q"
                            elif low_val == "light": uz_obj[k] = "Yorqin"
                            elif low_val == "name": uz_obj[k] = "Nom"
                            elif low_val == "value": uz_obj[k] = "Qiymat"
                            elif low_val == "title": uz_obj[k] = "Sarlavha"

        elif isinstance(uz_obj, list):
            for i, item in enumerate(uz_obj):
                if i < len(en_obj):
                    translate_recursive(item, en_obj[i], path)

    translate_recursive(uz_data, en_data)

    with open(uz_path, 'w', encoding='utf-8') as f:
        json.dump(uz_data, f, indent=2, ensure_ascii=False)

translations = {
    "Common.Controllers.Shortcuts.txtDescriptionSpecialOptionsKeepSourceFormat": "Nusxalangan matnning asl formatini saqlang.",
    "Common.Controllers.Shortcuts.txtDescriptionSpecialOptionsKeepTextOnly": "Matnni asl formatini saqlamasdan joylashtiring.",
    "Common.Controllers.Shortcuts.txtDescriptionSpecialOptionsNestTable": "Nusxalangan jadvalni mavjud yacheyka ichiga ichma-ich jadval sifatida joylashtiring.",
    "Common.Controllers.Shortcuts.txtDescriptionSpecialOptionsOverwriteCells": "Mavjud jadval tarkibini nusxalangan ma'lumotlar bilan almashtiring.",
    "Common.Controllers.Shortcuts.txtDescriptionSpeechWorker": "Ekran o'quvchi dasturlar (screen readers) uchun ilovada bajarilgan amallarni uzatishni yoqadi/o'chiradi.",
    "Common.Controllers.Shortcuts.txtDescriptionStartIndent": "Ro'yxat/surish darajasini oshiring (kursor paragraf boshida bo'lganda).",
    "Common.Controllers.Shortcuts.txtDescriptionStartUnIndent": "Ro'yxat/surish darajasini kamaytiring (kursor paragraf boshida bo'lganda).",
    "Common.Controllers.Shortcuts.txtDescriptionStrikeout": "Tanlangan matn qismini o'chirilgan (ustidan chiziq tortilgan) qiling.",
    "Common.Controllers.Shortcuts.txtDescriptionSubscript": "Tanlangan matn qismini kichraytiring va qatorning pastki qismiga joylashtiring (pastki indeks).",
    "Common.Controllers.Shortcuts.txtDescriptionSuperscript": "Tanlangan matn qismini kichraytiring va qatorning yuqori qismiga joylashtiring (yuqori indeks).",
    "Common.Controllers.Shortcuts.txtDescriptionTrademarkSign": "Joriy kursor turgan joyga savdo belgisi ramzini kiriting.",
    "Common.Controllers.Shortcuts.txtDescriptionUnderline": "Tanlangan matn qismining tagiga chizib chiqing.",
    "Common.Controllers.Shortcuts.txtDescriptionUnIndent": "Paragraf surilishini chap tomondan bosqichma-bosqich kamaytiring.",
    "Common.Controllers.Shortcuts.txtDescriptionUpdateFields": "Maydonlarni yangilang (masalan, Mundarija).",
    "Common.Controllers.Shortcuts.txtDescriptionVisitHyperlink": "Havolaga o'ting (kursor havola ustida bo'lganda).",
    "Common.Controllers.Shortcuts.txtDescriptionZoom100": "Masshtabni standart 100% holatiga qaytaring.",
    "Common.Controllers.Shortcuts.txtDescriptionZoomIn": "Hujjatni yaqinlashtiring.",
    "Common.Controllers.Shortcuts.txtDescriptionZoomOut": "Hujjatni uzoqlashtiring.",
    "Common.Views.AutoCorrectDialog.textAdd": "Qo'shish",
    "Common.Views.AutoCorrectDialog.textApplyText": "Yozish vaqtida qo'llash",
    "Common.Views.AutoCorrectDialog.textAutoCorrect": "Matnni avtomatik tuzatish",
    "Common.Views.AutoCorrectDialog.textAutoFormat": "Yozish vaqtida avtomatik formatlash",
    "Common.Views.AutoCorrectDialog.textBulleted": "Avtomatik belgili ro'yxatlar",
    "Common.Views.AutoCorrectDialog.textBy": "Bilan",
    "Common.Views.AutoCorrectDialog.textDelete": "O'chirish",
    "Common.Views.AutoCorrectDialog.textDoubleSpaces": "Ikki marta bo'sh joy bosilganda nuqta qo'shish",
    "Common.Views.AutoCorrectDialog.textFLCells": "Jadval yacheykalarida birinchi harfni katta qiling",
    "Common.Views.AutoCorrectDialog.textFLDont": "Shundan keyin katta harf qilinmasin",
    "Common.Views.AutoCorrectDialog.textFLSentence": "Gaplarning birinchi harfini katta qiling",
    "Common.Views.AutoCorrectDialog.textForLangFL": "Til uchun istisnolar:",
    "Common.Views.AutoCorrectDialog.textHyperlink": "Internet va tarmoq yo'llariga havolalar",
    "Common.Views.AutoCorrectDialog.textHyphens": "Defislarni (--) tire (—) bilan almashtirish",
    "Common.Views.AutoCorrectDialog.textMathCorrect": "Matematik avtomatik tuzatish",
    "Common.Views.AutoCorrectDialog.textNumbered": "Avtomatik raqamlangan ro'yxatlar",
    "Common.Views.AutoCorrectDialog.textQuotes": "\"To'g'ri qo'shtirnoqlar\"ni \"egri qo'shtirnoqlar\"ga almashtirish",
    "Common.Views.AutoCorrectDialog.textReplace": "Almashtirish",
    "DE.Controllers.Toolbar.txtSymbol_celsius": "Selsiy darajasi",
    "DE.Controllers.Toolbar.txtSymbol_chi": "Xi",
    "DE.Controllers.Toolbar.txtSymbol_cong": "Taxminan teng",
    "DE.Controllers.Toolbar.txtSymbol_cup": "Birlashma",
    "DE.Controllers.Toolbar.txtSymbol_degree": "Darajalar",
    "DE.Controllers.Toolbar.txtSymbol_div": "Bo'lish belgisi",
    "DE.Controllers.Toolbar.txtSymbol_downarrow": "Pastga strelka",
    "DE.Controllers.Toolbar.txtSymbol_emptyset": "Bo'sh to'plam",
    "DE.Controllers.Toolbar.txtSymbol_equals": "Teng",
    "DE.Controllers.Toolbar.txtSymbol_equiv": "Identik",
    "DE.Controllers.Toolbar.txtSymbol_exists": "Mavjudlik kvantori",
    "DE.Controllers.Toolbar.txtSymbol_factorial": "Faktorial",
    "DE.Controllers.Toolbar.txtSymbol_fahrenheit": "Faringeyt darajasi",
    "DE.Controllers.Toolbar.txtSymbol_forall": "Barcha uchun",
    "DE.Controllers.Toolbar.txtSymbol_geq": "Katta yoki teng",
    "DE.Controllers.Toolbar.txtSymbol_gg": "Ancha katta",
    "DE.Controllers.Toolbar.txtSymbol_greater": "Katta",
    "DE.Controllers.Toolbar.txtSymbol_in": "Tegishli",
    "DE.Controllers.Toolbar.txtSymbol_inc": "O'sish (inkrement)",
    "DE.Controllers.Toolbar.txtSymbol_infinity": "Cheksizlik",
    "DE.Controllers.Toolbar.txtSymbol_leftarrow": "Chapga strelka",
    "DE.Controllers.Toolbar.txtSymbol_leftrightarrow": "Ikki tomonlama strelka",
    "DE.Controllers.Toolbar.txtSymbol_leq": "Kichik yoki teng",
    "DE.Controllers.Toolbar.txtSymbol_less": "Kichik",
    "DE.Controllers.Toolbar.txtSymbol_ll": "Ancha kichik",
    "DE.Controllers.Toolbar.txtSymbol_minus": "Minus",
    "DE.Controllers.Toolbar.txtSymbol_neq": "Teng emas",
    "DE.Controllers.Toolbar.txtSymbol_not": "Inkor belgisi",
    "DE.Controllers.Toolbar.txtSymbol_notexists": "Mavjud emas",
    "DE.Controllers.Toolbar.txtSymbol_percent": "Foiz",
    "DE.Controllers.Toolbar.txtSymbol_plus": "Plyus",
    "DE.Controllers.Toolbar.txtSymbol_rightarrow": "O'ngga strelka",
    "DE.Controllers.Toolbar.txtSymbol_sqrt": "Ildiz belgisi",
    "DE.Controllers.Toolbar.txtSymbol_therefore": "Shuning uchun",
    "DE.Controllers.Toolbar.txtSymbol_times": "Ko'paytirish belgisi",
    "DE.Controllers.Toolbar.txtSymbol_uparrow": "Yuqoriga strelka",
    "DE.Controllers.Viewport.textFitPage": "Sahifaga moslashtirish",
    "DE.Controllers.Viewport.textFitWidth": "Kenglikka moslashtirish",
    "DE.Controllers.Viewport.txtDarkMode": "Tungi rejim",
    "DE.Views.BookmarksDialog.textAdd": "Qo'shish",
    "DE.Views.BookmarksDialog.textBookmarkName": "Xatcho'p nomi",
    "COMMON.Views.SearchDialog.textReplaceAll": "Hammasini almashtirish",
    "Common.Translation.textMoreButton": "Ko'proq",
    "Common.UI.Window.okButtonText": "OK",
    "Common.UI.Window.cancelButtonText": "Bekor qilish",
    "Common.UI.Window.yesButtonText": "Ha",
    "Common.UI.Window.noButtonText": "Yo'q",
    "Common.Views.Comments.textAddReply": "Javob qo'shish",
    "Common.Views.Comments.textAddComment": "Izoh qo'shish",
    "Common.Views.OpenDialog.txtEncoding": "Kodlash",
    "Common.Views.OpenDialog.txtIncorrectPwd": "Parol noto'g'ri.",
    "Common.Views.OpenDialog.txtOpenFile": "Faylni ochish uchun parolni kiriting",
    "Common.Views.OpenDialog.txtPassword": "Parol",
    "Common.Views.OpenDialog.txtPreview": "Ko'rinish",
    "Common.Views.PasswordDialog.txtDescription": "Ushbu hujjatni himoya qilish uchun parol o'rnating",
    "Common.Views.PasswordDialog.txtRepeat": "Parol takrorlang",
    "Common.Views.PasswordDialog.txtTitle": "Parol o'rnatish",
    "Common.Views.Plugins.textBackgroundPlugins": "Fon plaginlari",
    "Common.Views.Plugins.textSettings": "Sozlamalar",
    "Common.Views.Plugins.textStart": "Ishga tushirish",
    "Common.Views.Plugins.textStop": "To'xtatish",
    "Common.Views.Protection.txtAddPwd": "Parol qo'shish",
    "Common.Views.Protection.txtChangePwd": "Parolni o'zgartirish",
    "Common.Views.Protection.txtDeletePwd": "Parolni o'chirish",
    "Common.Views.RecentFiles.txtOpenRecent": "Oxirgi fayllarni ochish",
    "Common.Views.RenameDialog.textName": "Fayl nomi",
    "Common.Views.ReviewChanges.txtAccept": "Qabul qilish",
    "Common.Views.ReviewChanges.txtReject": "Rad etish",
    "Common.Views.ReviewChanges.mniSettings": "Solishtirish sozlamalari",
    "Common.Views.ReviewChanges.strFast": "Tezkor (Fast)",
    "Common.Views.ReviewChanges.strStrict": "Qat'iy (Strict)",
    "Common.Views.ReviewChanges.tipAcceptCurrent": "Joriy o'zgarishni qabul qilish va keyingisiga o'tish",
    "Common.Views.ReviewChanges.tipRejectCurrent": "Joriy o'zgarishni rad etish va keyingisiga o'tish",
    "Common.Views.ReviewChanges.tipHistory": "Versiyalar tarixini ko'rsatish",
    "Common.Views.ReviewChanges.tipCompare": "Joriy hujjatni boshqasi bilan solishtirish",
    "Common.Views.ReviewChanges.tipReview": "O'zgarishlarni kuzatish",
    "Common.Views.ReviewChanges.tipSharing": "Hujjatga kirish huquqlarini boshqarish",
    "Common.Views.ReviewChanges.tipSetSpelling": "Imloni tekshirish",
    "Common.Views.ReviewChanges.tipSetDocLang": "Hujjat tilini sozlash",
    "Common.Views.ReviewChanges.textEnable": "Yoqish",
    "Common.Views.Shortcuts.txtLabelBold": "Qalin",
    "Common.Views.Shortcuts.txtLabelItalic": "Kursiv",
    "Common.Views.Shortcuts.txtLabelUnderline": "Tagiga_chizilgan",
    "Common.Views.Shortcuts.txtLabelSave": "Saqlash",
    "Common.Views.Shortcuts.txtLabelCopy": "Nusxalash",
    "Common.Views.Shortcuts.txtLabelCut": "Kesib_olish",
    "Common.Views.Shortcuts.txtLabelPaste": "Joylashtirish",
    "Common.Views.Shortcuts.txtLabelUndo": "Bekor_qilish",
    "Common.Views.Shortcuts.txtLabelRedo": "Takrorlash",
    "Common.Views.Shortcuts.txtLabelEditSelectAll": "Hammasini_tanlash",
    "Common.UI.SearchBar.textFind": "Topish",
    "Common.UI.SearchBar.tipNextResult": "Keyingi natija",
    "Common.UI.SearchBar.tipPreviousResult": "Oldingi natija",
    "Common.UI.SearchBar.tipCloseSearch": "Qidiruvni yopish",
    "Common.UI.SearchDialog.textFind": "Topish",
    "Common.UI.SearchDialog.textReplace": "Almashtirish",
    "Common.UI.SearchDialog.textReplaceAll": "Hammasini almashtirish",
    "Common.UI.SearchDialog.textHighlight": "Izlash natijalarini ajratib ko'rsatish",
    "Common.UI.SearchDialog.textMatchCase": "Katta-kichik harflar",
    "Common.UI.SearchDialog.textWholeWords": "Faqat butun so'z",
    "Common.UI.SearchDialog.txtBtnReplace": "Almashtirish",
    "Common.UI.SearchDialog.txtBtnReplaceAll": "Hammasini almashtirish",
    "Common.UI.SearchDialog.txtBtnHideReplace": "Almashtirishni yashirish",
    "Common.UI.SearchDialog.textSearchStart": "Qidiruvni shu yerdan boshlang",
    "Common.UI.SearchDialog.textReplaceDef": "Almashtirish uchun matn",
    "Common.Views.History.txtErrorLoadHistory": "Tarixni yuklab bo'lmadi",
    "Common.Views.History.txtVersion": "Versiya",
    "Common.Views.History.txtAuthor": "Muallif",
    "Common.Views.History.txtDate": "Sana",
    "Common.Views.RenameDialog.txtInvalidName": "Fayl nomi quyidagi belgilarni o'z ichiga olishi mumkin emas: ",
    "Common.UI.Window.textConfirmation": "Tasdiqlash",
    "Common.UI.Window.textWarning": "Ogohlantirish",
    "Common.UI.Window.textError": "Xato",
    "Common.UI.Window.textInformation": "Ma'lumot",
    "Common.UI.Window.closeButtonText": "Yopish",
    "Common.UI.Window.saveButtonText": "Saqlash",
    "Common.UI.Window.downloadButtonText": "Yuklab olish",
    "Common.UI.Window.printButtonText": "Chop etish",
    "Common.UI.Window.applyButtonText": "Qo'llash",
    "Common.UI.Window.deleteButtonText": "O'chirish",
    "Common.UI.Window.clearButtonText": "Tozalash",
    "Common.UI.Window.resetButtonText": "Tashlash",
    "Common.UI.Window.nextButtonText": "Keyingi",
    "Common.UI.Window.backButtonText": "Orqaga",
    "Common.UI.Window.finishButtonText": "Tugatish",
    "Common.UI.Window.okButtonText": "OK",
    "Common.UI.Window.cancelButtonText": "Bekor qilish",
    "Common.UI.Window.yesButtonText": "Ha",
    "Common.UI.Window.noButtonText": "Yo'q",
    "Common.Views.About.txtVersion": "Versiya ",
    "Common.Views.About.txtPoweredBy": "Tomonidan ishlab chiqilgan",
    "Common.Views.About.txtAddress": "manzil: ",
    "Common.Views.About.txtTel": "tel.: ",
    "Common.Views.About.txtMail": "email: ",
    "Common.Views.About.txtLicensee": "LITSENZIAT",
    "Common.Views.About.txtLicensor": "LITSENZIAR",
    "Common.Views.Comment.textAddComment": "Izoh qo'shish",
    "Common.Views.Comment.textAddReply": "Javob berish",
    "Common.Views.Comment.textDelete": "O'chirish",
    "Common.Views.Comment.textEdit": "Tahrirlash",
    "Common.Views.Comment.textResolve": "Hal qilish",
    "Common.Views.Comment.textResolved": "Hal qilingan",
    "Common.Views.Common.textLoading": "Yuklanmoqda...",
    "Common.Views.Common.textError": "Xatolik yuz berdi",
    "Common.Views.Common.textSuccess": "Muvaffaqiyatli bajarildi",
    "Common.Views.Common.textWarning": "Ogohlantirish",
    "Common.Views.Common.textNone": "Yo'q",
    "Common.Views.Common.textAuto": "Avto",
    "Common.Views.Common.textCustom": "Maxsus",
    "Common.Views.Common.textDefault": "Standart",
    "Common.Views.Common.textTransparent": "Shaffof",
    "Common.Views.Common.textColor": "Rang",
    "Common.Views.Common.textWidth": "Kenglik",
    "Common.Views.Common.textHeight": "Balandlik",
    "Common.Views.Common.textSize": "O'lcham",
    "Common.Views.Common.textStyle": "Uslub",
    "Common.Views.Common.textType": "Tur",
    "Common.Views.Common.textName": "Nom",
    "Common.Views.Common.textValue": "Qiymat",
    "Common.Views.File.textNew": "Yangi",
    "Common.Views.File.textOpen": "Ochish",
    "Common.Views.File.textSave": "Saqlash",
    "Common.Views.File.textSaveAs": "Sifatida saqlash",
    "Common.Views.File.textPrint": "Chop etish",
    "Common.Views.File.textShare": "Ulashish",
    "Common.Views.File.textDownload": "Yuklab olish",
    "Common.Views.File.textClose": "Yopish",
    "Common.Views.File.textRecent": "Oxirgilari",
    "Common.Views.File.textHelp": "Yordam",
    "Common.Views.File.textSettings": "Sozalamalar",
    "Common.Views.File.textInfo": "Ma'lumot",
    "Common.Views.Filter.textAll": "Hammasi",
    "Common.Views.Filter.textClear": "Tozalash",
    "Common.Views.Filter.textApply": "Qo'llash",
    "Common.Views.Filter.textCancel": "Bekor qilish",
    "Common.Views.Filter.textSearch": "Qidiruv",
    "Common.Views.Filter.textSelected": "Tanlangan",
    "Common.Views.Filter.textEmpty": "Bo'sh",
    "Common.Views.Hyperlink.textLink": "Havola",
    "Common.Views.Hyperlink.textUrl": "URL",
    "Common.Views.Hyperlink.textDisplay": "Ko'rinadigan matn",
    "Common.Views.Hyperlink.textTip": "Maslahat",
    "Common.Views.Hyperlink.textTitle": "Gipersilka",
    "Common.Views.Hyperlink.textTarget": "Nishon",
    "Common.Views.Hyperlink.textCurrent": "Joriy hujjat",
    "Common.Views.Hyperlink.textExisting": "Mavjud fayl yoki veb-sahifa",
    "Common.Views.Image.textInsert": "Rasmni joylashtirish",
    "Common.Views.Image.textFromFile": "Fayldan",
    "Common.Views.Image.textFromUrl": "URL bo'yicha",
    "Common.Views.Image.textFromStorage": "Xotiradan",
    "Common.Views.Image.textChange": "Rasmni o'zgartirish",
    "Common.Views.Image.textEdit": "Rasm tahrirlash",
    "Common.Views.Image.textTitle": "Rasm",
    "Common.Views.Layout.textPage": "Sahifa",
    "Common.Views.Layout.textMargins": "Maydonlar",
    "Common.Views.Layout.textOrientation": "Yo'nalish",
    "Common.Views.Layout.textPortrait": "Kitob",
    "Common.Views.Layout.textLandscape": "Albom",
    "Common.Views.Layout.textSize": "O'lcham",
    "Common.Views.Layout.textColumns": "Ustunlar",
    "Common.Views.Layout.textBreaks": "Uzilishlar",
    "Common.Views.Layout.textHeader": "Yuqori kolontitul",
    "Common.Views.Layout.textFooter": "Pastki kolontitul",
    "Common.Views.Layout.textNumbers": "Sahifa raqamlari",
    "Common.Views.Layout.textWatermark": "Suv belgisi",
    "Common.Views.List.textNumbered": "Raqamlangan ro'yxat",
    "Common.Views.List.textBulleted": "Belgili ro'yxat",
    "Common.Views.List.textMultilevel": "Ko'p darajali ro'yxat",
    "Common.Views.List.textNone": "Yo'q",
    "Common.Views.Plugins.textPlugins": "Plaginlar",
    "Common.Views.Plugins.textManager": "Plaginlar menejeri",
    "Common.Views.Plugins.textSettings": "Sozlamalar",
    "Common.Views.Protection.textTitle": "Himoya",
    "Common.Views.Protection.textPassword": "Parol",
    "Common.Views.Protection.textConfirm": "Parolni tasdiqlang",
    "Common.Views.Protection.textLock": "Qulflash",
    "Common.Views.Protection.textUnlock": "Qulfdan chiqarish",
    "Common.Views.Review.textTrackChanges": "O'zgarishlarni kuzatish",
    "Common.Views.Review.textAccept": "Qabul qilish",
    "Common.Views.Review.textReject": "Rad etish",
    "Common.Views.Review.textNext": "Keyingi",
    "Common.Views.Review.textPrev": "Oldingi",
    "Common.Views.Review.textSpelling": "Imlo",
    "Common.Views.Review.textLanguage": "Til",
    "Common.Views.Review.textComments": "Izohlar",
    "Common.Views.Search.textFind": "Topish",
    "Common.Views.Search.textReplace": "Almashtirish",
    "Common.Views.Search.textFindAll": "Hamma topilsin",
    "Common.Views.Search.textReplaceAll": "Hammasini almashtirish",
    "Common.Views.Search.textMatchCase": "Katta-kichik harflarni farqlash",
    "Common.Views.Search.textWholeWord": "Faqat butun so'z",
    "Common.Views.Table.textInsert": "Jadvalni joylashtirish",
    "Common.Views.Table.textTable": "Jadval",
    "Common.Views.Table.textRows": "Qatorlar",
    "Common.Views.Table.textCols": "Ustunlar",
    "Common.Views.Table.textCells": "Yacheykalar",
    "Common.Views.Table.textMerge": "Yacheykalarni birlashtirish",
    "Common.Views.Table.textSplit": "Yacheykalarni ajratish",
    "Common.Views.Table.textProperties": "Jadval xususiyatlari",
    "Common.Views.View.textView": "Ko'rinish",
    "Common.Views.View.textZoom": "Masshtab",
    "Common.Views.View.textFitPage": "Sahifaga moslash",
    "Common.Views.View.textFitWidth": "Kenglikka moslash",
    "Common.Views.View.textFull": "To'liq ekran",
    "Common.Views.View.textRulers": "Liniykalar",
    "Common.Views.View.textGrid": "Setka",
    "Common.Views.View.textDarkMode": "Tungi rejim",
    "Common.Views.View.textLightMode": "Kunduzgi rejim",
    "Common.Views.Table.textTotalRow": "Jami qatori",
    "Common.Views.Table.textFirstCol": "Birinchi ustun",
    "Common.Views.Table.textLastCol": "Oxirgi ustun",
    "Common.UI.ButtonColored.textAutoColor": "Avtomatik rang",
    "Common.UI.ButtonColored.textEyedropper": "Pipetka",
    "Common.UI.ButtonColored.textNewColor": "Boshqa ranglar",
    "Common.UI.ComboBorderSize.txtNoBorders": "Chegarasiz",
    "Common.UI.SearchDialog.textTitle": "Topish va almashtirish",
    "Common.Utils.Metric.txtCm": "sm",
    "Common.Utils.Metric.txtPt": "pt",
    "Common.Utils.String.textCtrl": "Ctrl",
    "Common.Utils.String.textShift": "Shift",
    "Common.Utils.String.textAlt": "Alt",
    "Common.Utils.ThemeColor.txtBlack": "Qora",
    "Common.Utils.ThemeColor.txtWhite": "Oq",
    "Common.Utils.ThemeColor.txtRed": "Qizil",
    "Common.Utils.ThemeColor.txtBlue": "Ko'k",
    "Common.Utils.ThemeColor.txtGreen": "Yashil",
    "Common.Utils.ThemeColor.txtYellow": "Sariq",
    "Common.Utils.ThemeColor.txtOrange": "To'q sariq",
    "Common.Utils.ThemeColor.txtPurple": "Binafsha",
    "Common.Utils.ThemeColor.txtGray": "Kulrang",
    "Common.Utils.ThemeColor.txtBrown": "Jigarrang",
    "Common.Views.AutoCorrectDialog.textTitle": "Avtotuzatish sozlamalari",
    "Common.Views.Chat.textChat": "Chat",
    "Common.Views.Chat.textSend": "Yuborish",
    "Common.Views.Chat.textEnterMessage": "Xabarni kiriting",
    "Common.Views.Comments.textAll": "Hammasi",
    "Common.Views.Comments.textResolved": "Hal qilingan",
    "Common.Views.ExtendedColorDialog.textNew": "Yangi",
    "Common.Views.ExtendedColorDialog.textCurrent": "Joriy",
    "Common.Views.ExtendedColorDialog.addButtonText": "Qo'shish",
    "Common.Views.ExternalLinks.textUpdate": "Yangilash",
    "Common.Views.ExternalLinks.textDontUpdate": "Yangilamaslik",
    "Common.Views.OpenDialog.textOpen": "Ochish",
    "Common.Views.OpenDialog.txtTitle": "Faylni ochish",
    "Common.Views.Plugins.textPluginsSuccessfullyInstalled": "Plaginlar muvaffaqiyatli o'rnatildi",
    "Common.Views.SearchDialog.textFind": "Topish",
    "Common.Views.SearchDialog.textReplace": "Almashtirish",
    "Common.Views.SynchronizeTip.textGotIt": "Tushunarli",
    "Common.Views.Themes.txtThemeLight": "Yorqin",
    "Common.Views.Themes.txtThemeDark": "To'q",
    "Common.Views.Themes.txtThemeSystem": "Tizim kabi",
    "DE.Views.Common.textFind": "Topish",
    "DE.Views.Common.textReplace": "Almashtirish",
    "DE.Views.Common.textGoTo": "O'tish",
    "DE.Views.Common.textPage": "Sahifa",
    "SSE.Views.Common.textCell": "Yacheyka",
    "SSE.Views.Common.textSheet": "Varaq",
    "PE.Views.Common.textSlide": "Slayd",
    "PE.Views.Common.textPresentation": "Prezentatsiya",
    "Common.Translation.textLanguage": "Til"
}

apps_dir = r"c:\Users\k_hasanov\Downloads\build_tools-master\build_tools-master\web-apps\apps"

for root, dirs, files in os.walk(apps_dir):
    if "en.json" in files and "uz.json" in files:
        en_path = os.path.join(root, "en.json")
        uz_path = os.path.join(root, "uz.json")
        print(f"Updating {uz_path}...")
        update_locale(uz_path, en_path, translations)

# Transliteration to Cyrillic
import re

def transliterate_uz(text):
    if not isinstance(text, str):
        return text
    mapping = {
        "sh": "ш", "Sh": "Ш", "SH": "Ш",
        "ch": "ч", "Ch": "Ч", "CH": "Ч",
        "o'": "ў", "O'": "Ў", "o’": "ў", "O’": "Ў", "o`": "ў", "O`": "Ў",
        "g'": "ғ", "G'": "Ғ", "g’": "ғ", "G’": "Ғ", "g`": "ғ", "G`": "Ғ",
        "yu": "ю", "Yu": "Ю", "YU": "Ю",
        "ya": "я", "Ya": "Я", "YA": "Я",
        "yo": "ё", "Yo": "Ё", "YO": "Ё",
        "ts": "ц", "Ts": "Ц", "TS": "Ц",
    }
    single_mapping = {
        'a': 'а', 'b': 'б', 'd': 'д', 'f': 'ф', 'g': 'г', 'h': 'ҳ', 'i': 'и', 'j': 'ж', 'k': 'к',
        'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о', 'p': 'п', 'q': 'қ', 'r': 'р', 's': 'с', 't': 'т', 'u': 'у',
        'v': 'в', 'w': 'в', 'x': 'х', 'y': 'й', 'z': 'з', 'A': 'А', 'B': 'Б', 'D': 'Д', 'F': 'Ф', 'G': 'Г',
        'H': 'Ҳ', 'I': 'И', 'J': 'Ж', 'K': 'К', 'L': 'Л', 'M': 'М', 'N': 'Н', 'O': 'О', 'P': 'П', 'Q': 'Қ',
        'R': 'Р', 'S': 'С', 'T': 'Т', 'U': 'У', 'V': 'В', 'W': 'В', 'X': 'Х', 'Y': 'Й', 'Z': 'З', "'": "ъ"
    }
    vowels = "aeiouAEOIU'’`"
    words = re.split(r'(\W+)', text)
    processed_words = []
    for word in words:
        if not word or not word[0].isalpha():
            processed_words.append(word)
            continue
        new_word = ""
        for i, char in enumerate(word):
            lower_char = char.lower()
            if lower_char == 'e':
                if i == 0 or (i > 0 and word[i-1].lower() in vowels):
                    new_word += 'Э' if char.isupper() else 'э'
                else:
                    new_word += 'Е' if char.isupper() else 'е'
            else:
                new_word += char
        processed_words.append(new_word)
    text = "".join(processed_words)
    res = text
    for lat, cyr in mapping.items(): res = res.replace(lat, cyr)
    for lat, cyr in single_mapping.items(): res = res.replace(lat, cyr)
    return res

def transliterate_recursive(obj):
    if isinstance(obj, dict):
        return {k: transliterate_recursive(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [transliterate_recursive(v) for v in obj]
    else:
        return transliterate_uz(obj)

for root, dirs, files in os.walk(apps_dir):
    if "uz.json" in files:
        uz_path = os.path.join(root, "uz.json")
        cyrl_path = os.path.join(root, "uz-cyrl.json")
        with open(uz_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        cyrl_data = transliterate_recursive(data)
        with open(cyrl_path, 'w', encoding='utf-8') as f:
            json.dump(cyrl_data, f, indent=2, ensure_ascii=False)
        print(f"Sync Cyrl: {cyrl_path}")

print("All translations and transliterations complete.")
