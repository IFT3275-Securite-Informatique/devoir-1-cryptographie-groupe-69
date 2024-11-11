from collections import defaultdict
import requests



def load_text_from_web(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while loading the text from {url}: {e}")
        return None

def frequence(C, longOctet=8):
    comptFreq = defaultdict(int)
    index = 0
    while index < len(C):
        segment = C[index:index + longOctet]
        if len(segment) == longOctet:
            comptFreq[segment] += 1
        index += longOctet
    comptOrganiser = dict(sorted(comptFreq.items(), key=lambda item: (-item[1], item[0])))
    return comptOrganiser


def dechiffre(textChiffrer, textRef, longOctet=8):
    freqChiffrer = frequence(textChiffrer, longOctet)
    freqRef = frequence(textRef, longOctet)

    totalFreqChiffrer = sum(freqChiffrer.values())
    totalFreqRef = sum(freqRef.values())
    freqCPonderer = {segmentChiffrer: occurrence / totalFreqChiffrer for segmentChiffrer, occurrence in freqChiffrer.items()}
    freqRPonderer = {segmentRef: occurrence / totalFreqRef for segmentRef, occurrence in freqRef.items()}

    cle = {}
    refUtiliser = set()
    for segmentChiffrer, poidChiffrer in sorted(freqCPonderer.items(), key=lambda item: -item[1]):
        segmentCorrespondant = None
        ecartMin = float('inf')
        for segmentRef, poidRef in freqRPonderer.items():
            if segmentRef in refUtiliser:
                continue
            ecart = abs(poidChiffrer - poidRef)
            if ecart < ecartMin:
                segmentCorrespondant = segmentRef
                ecartMin = ecart
        if segmentCorrespondant:
            cle[segmentChiffrer] = segmentCorrespondant
            refUtiliser.add(segmentCorrespondant)

    segmentsDechiffres = []
    for i in range(0, len(textChiffrer), longOctet):
        segment = textChiffrer[i:i + longOctet]
        if segment in cle:
            segmentsDechiffres.append(cle[segment])
        else:
            segmentsSimilaires = [seg for seg in cle if seg.startswith(segment[:4])]
            if segmentsSimilaires:
                segmentsDechiffres.append(cle[segmentsSimilaires[0]])
            else:
                segmentsDechiffres.append('?')
    messageDechiffre = ''.join(segmentsDechiffres)
    return messageDechiffre


def decrypt(C):
    reference_url = "https://www.gutenberg.org/ebooks/13846.txt.utf-8"
    textRef = load_text_from_web(reference_url)
    M = dechiffre(C, textRef)
    return M