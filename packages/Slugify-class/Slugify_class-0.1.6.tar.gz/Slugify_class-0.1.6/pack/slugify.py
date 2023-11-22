
class Slugify:
    def __init__(self, ramplasman="-"):
        self.ramplasman = ramplasman
        self.lis = "abcdefghijklmnopqrstuvwxyz1234567890-"
        self.accent_mapping = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                               'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
                               'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ñ': 'n', 'ç': 'c'}

    def text_to_slug(self, chen):
        chen = chen.lower()
        chen = retire_accent().retirer_accent(chen)
        chen = ''.join(c if c in self.lis else self.ramplasman for c in chen)
        chen=retire_doublon().retire_doublon(chen)
        return chen
    
class retire_accent:
    def __init__(self, ramplasman="-"):
        self.accent_mapping = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                               'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
                               'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ñ': 'n', 'ç': 'c'}
    def retirer_accent(self, chen):
        chen_san_aksan = ''.join(self.accent_mapping.get(c, c) for c in chen)
        return chen_san_aksan


class retire_doublon:
    def __init__(self, ramplasman="-"):
        self.ramplasman = ramplasman
    def retire_doublon(self, chen):
        i = 0
        while i < len(chen) - 1:
            chen_list = list(chen)
            if chen[i] == self.ramplasman and chen[i - 1] == self.ramplasman:
                chen_list.pop(i)
                chen = ''.join(chen_list)
                i = 0
            i += 1
        return chen
# if __name__ == "__main__":
#     text_processor = Slugify()
#     texte = "Nenpòt text la li ye mèt @@@gen aksan"
# #     texte_san_aksan = text_processor.retirer_accent(texte)
#     texte_slugifie = text_processor.text_to_slug(texte)
# # #     texte_slugifie=text_processor.retire_doublon(texte_slugifie)
#     print(texte_slugifie)
