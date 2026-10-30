"""Contract for the complete written five-star review audit, 30 October 2026.

Pinned identities come from the independently verified Google listing audits.
Execute the real browser data script so broken exports and mutable data fail too.
"""
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "google-reviews-data.js"
BRANCH_URLS = {
    "corniche": "https://www.google.com/maps/place/?q=place_id:ChIJgb-kmGNmXj4R6fUFteS1G_U",
    "al-raha": "https://www.google.com/maps/place/Al+Raha+Branch+-+Dr.+Mohamed+Munir+Dental+Centre+-+LLC/@24.4388317,54.5744795,997m/data=!3m1!1e3!4m8!3m7!1s0x3e5e450061f92b85:0xb6d18f896de894bd!8m2!3d24.4388317!4d54.5744795!9m1!1b1"
}
# [Google review ID, Google reviewer spelling, listing branch, age at audit].
AUDITED_IDENTITIES = json.loads(r'''
[
  ["Ci9DQUlRQUNvZENodHljRjlvT2s4NGJWTnRhRkJqY2paaGMzcDNVRTF0YW14cVlXYxAB","Antoni Yousef","corniche","8 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25WVE1YTkJTVk5wTFhOaVJXNW9SRzE2UVhkNlVFRRAB","Fay Shaw","corniche","6 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xaSlRWRTJSSFV4YzBZM2NuVjFRM2cwU0hGUFgzYxAB","Emily Campbell Scully","corniche","5 months ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNPaWUtbzBnRRAB","Waleed Humaid","corniche","4 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pGb1RGTllaMmxWVVdsRFprRmlNbXh5V21OVVEwRRAB","Twana Karim","corniche","a year ago"],
  ["ChRDSUhNMG9nS0VJQ0FnSUNEajZVVxAB","Joycefe Graciosa","corniche","2 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pkYVVtOURkVXN4V2pWdmExTjBRbGxFWW5OWlZGRRAB","Kari Felton","corniche","11 months ago"],
  ["ChZDSUhNMG9nS0VKYkMxZl9zMzdDM0pBEAE","Omar Muflahi","corniche","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2sxU1FVSkRSMmRFTm1oR1NHZE9Na1pIYVRZemJuYxAB","Adela Askandar","corniche","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2s1NVlUSktTMko1UlVGaFkzcEtSWEZuZEVWdGVIYxAB","el missouri Faiza","corniche","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT20xS05WVmlXRFpTZVZSdVNqQndlV3R4Wm1sRWJtYxAB","RachelT","corniche","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pWUmVEQmtiMGRmV2pGaVIyWm5jR1J5ZUY5bVNYYxAB","Zainab Mansour","corniche","11 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21nNFFXbEpRMFJYWkdGaVZ6UmhhVk13Y2xGdlZHYxAB","Safeya Al Hameli","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VPeWlrSWJUckxiOUxnEAE","Mohammed Mazrooei","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNUd1pPN1JBEAE","joseph saoud","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURodHBDeXVnRRAB","AREDEL JR_FAM","corniche","Edited 2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPMmVfNEZnEAE","Waleed Humaid","corniche","4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsaU11WExBEAE","Ali Alomari","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJNms1THZyc1pPaFZ3EAE","Ilm X","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNwMTZUOWlBRRAB","Hala Ahmadieh","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPbGVPb2NBEAE","Panos Liatsis","corniche","4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNUM01mN1V3EAE","Radhika C","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNoazh6dm5RRRAB","Beth Marciniak","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNsanZxNWlBRRAB","Talal Al-Mukhalalati","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNQeXA2eDdRRRAB","Hadil Saifi","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURod19hU0JnEAE","Rina de la Cruz","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURPZ08tOXhRRRAB","Deema Jayousi","corniche","4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUN1NVlHRldREAE","Salama Al Mazrouie","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURKZ3Rfa3BRRRAB","nicholas wyon","corniche","Edited 2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURSaEp6R0hBEAE","Shamsa","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUQteW9uSnpRRRAB","ghassan hassan","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNseF9YNFJBEAE","Alreem","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUMxdWNieUtBEAE","alyaziaa","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPMjVIellREAE","Caroline Saatdjian","corniche","4 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25OQ09XZHlhblpFWkY5UVRXeFlUMXBaUVRSblRGRRAB","Sahar Alsalman","corniche","6 months ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURWLS1HVThRRRAB","Abu Abdullah","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUQ5MmN2ZmtRRRAB","Bareaa Kadah","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnTURBeDRlcjZ3RRAB","Alastair Nicholson","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCdXJfTXlBRRAB","noora alkamali","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURacW9lYU9REAE","MOHAMED Almansoori","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURHaE9LazV3RRAB","Houssam weiss","corniche","Edited 4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPdF8yYVNREAE","Marie Ghastine","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURoeHB2SnVRRRAB","Yasser Sallam","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCNXJfYTlBRRAB","Issam Agha","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCNHNQVm5nRRAB","Fatheya R","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURWZ1pIbEZ3EAE","Muna Aldhuhoori","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUMxLXFMQ0ZBEAE","Mubarak alketbi","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VKYWM2Nl8yaHF2bTJ3RRAB","Hidayah Al Zaabi","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnTURnMXNiNmdBRRAB","Rasha Radi","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsa2RpakNnEAE","Mohamed Mabrouk","corniche","2 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2toTmVWZHFlV1J5TlhSdGFqbFZVVlJUZVdodUxYYxAB","i ansari","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURSMU03WEZREAE","Dheyab BinHamoodah","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPbzdEVVd3EAE","Fahad SalZaabi","corniche","4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUQxeXZiNkxnEAE","A. H","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNoeFB6U0V3EAE","Khalifa Almheiri","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURMOXN6aE5nEAE","Mariam Alhammadi","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNaNUtDZUdREAE","S. J. AL QUBAISI","corniche","Edited 2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURsZ05qNzN3RRAB","Hessa Al Hashemi","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCbE9PcDN3RRAB","Etienne Berchtold","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURObU5DbTJnRRAB","Hissa alkhaja","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsaXU3dmNREAE","Amr Mezian","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNoa192aXN3RRAB","Marwa Sammour","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUMxazRibm9RRRAB","marchi 48","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUR4dXJfaURREAE","Ahmed Almehairi","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUMxOHJmZWtRRRAB","Rana Al Mukhtar","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUR4bXVEVXFnRRAB","ayman yatim","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNPbGFMdWtRRRAB","Sadir P K","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNPbGJMQmtRRRAB","shafeeq koolikad","corniche","4 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2s1eVNVUjFZak0xU20xWWJVZFdUSGRYUjFGR05GRRAB","وليد ابوعبدو","corniche","7 hours ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pCUFYzbGFkbFZ6YVRWaU9HOVNWV290WWpnNGFYYxAB","Emirati Mother","corniche","a week ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pOVVZsVlJhMkUwZW5NMFFsTlRZV3B6UkZkclJGRRAB","Mz2006","corniche","3 weeks ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25kM1ZFdDZZbTk2V1RVeU4wOVdibVF0ZDNSSGRFRRAB","Ba Zim","corniche","a month ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pNMk1tSjRUMjVCZEY5bmJGSlNTbVJZZURaSGRXYxAB","Victoriya Davydova","corniche","5 months ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNwbWI3YnF3RRAB","Anna Lona","corniche","3 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2taNWJHWmlibGhqTWpoRFR6RmhUMVZPUTI1SlYxRRAB","Sanaa Freihat","corniche","6 months ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNKNU9yUm53RRAB","IZZA Bouziane BD","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VLal92dEdvejhmNTZRRRAB","Noura Alm","corniche","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21STExVMVZjakpFVkRKd2VVVkVTazVCZFRKeGRWRRAB","reem awny","corniche","10 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2tzeFdFeERjbUV6V1RoRWN6aGhVVE5EZFhGd2FsRRAB","Bakheeta zayed","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsaDlEM09BEAE","Ahmed Al khouri","corniche","2 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2tsMVNrMUtaVlY1VjNFd1VGUkpZMFJLTW5NMFNXYxAB","Muna Alshuwaihi","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNUcF82OHN3RRAB","Husain ALJASMI","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VObWs0NURVeTZuTWxRRRAB","Z R","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNUOTdHNmhnRRAB","Samira Ahmed","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURWc2NHOGtBRRAB","Amal Shaker","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURkLVlqb2tRRRAB","Latifa alobeidli","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNKMjhENW1RRRAB","Moath Alsabty","corniche","Edited 3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCMnZYRC1BRRAB","Soheir El shall","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNod2Z2NnBRRRAB","Mahra 11","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURCcHVxZkFREAE","abdullah nourallah","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNRbWFuUDFBRRAB","AHMAD ALSHAMSI","corniche","8 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xwclZGOVlTME0yZGtSTlFuaG5NazlMYkV0MVgwRRAB","Haila 22","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURKZ01LLXRBRRAB","Anissa Nagati","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNBN0pPU253RRAB","J.A.A Alhameli","corniche","9 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUMwbE5lTmhBRRAB","علياء اليافعي","corniche","7 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURCNFBXOUhBEAE","muneera alkharousi","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNPMWE3T1BnEAE","Marwan Abu hashish","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURoZzhQcHpnRRAB","as00m as00m","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUR4bXZ5dnVBRRAB","Ali SM Almehairbi","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNCdjhiZm1BRRAB","Ferial Karmy","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsdnRDdENnEAE","S 7","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNkN3JqR29nRRAB","hamada Edris","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnTURvLTctVzJBRRAB","Moza Al Qubaisi","corniche","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURPMFBPMEd3EAE","Huwaidi Hadi","corniche","4 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURoeUxPWEJBEAE","Aroob Ghaizan","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURCdUstbkRBEAE","Abdalla Alsuwaidi","corniche","Edited 2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURodHRQNGVREAE","المانيا المانيا","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUQxcFo3dTR3RRAB","Fatima Juma","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURteDR1TTB3RRAB","zubaida ahmed","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNsM3Q2QTNnRRAB","Mema A","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNPMWJyMmh3RRAB","Marwani To","corniche","4 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUQxX2ZmQmdRRRAB","Mona Alobeidli_1","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSURCeXBldi1BRRAB","k m","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNsc3QyZVN3EAE","نبنين نبينين","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSURKc09tV1lnEAE","سلطان الساعدي","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNocTgzWWlBRRAB","om-salem Sem","corniche","3 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUQ4bDlTd1hREAE","مبارك المنصوري","corniche","6 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUR4NnJfS1B3EAE","Keokje Sweets","corniche","3 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNseDYtTHNnRRAB","Abdulla Alabdouli","corniche","2 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNseWFLUjZRRRAB","H H","corniche","2 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUQ4Zzl5TFF3EAE","anna lona","corniche","6 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUR2ZzdUakF3EAE","Sssa Almaz","corniche","a year ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNvdzl5RnFBRRAB","Moza Jassim","corniche","7 years ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUNBOUl2Q2VnEAE","Khalfan Almehairbi","corniche","8 years ago"],
  ["ChdDSUhNMG9nS0VJQ0FnSUNsMDR5cjZBRRAB","Mubarak640","corniche","2 years ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2s1Zk4wMDRNbGxSZGpockxXNUJia1l4Y2t0UFNXYxAB","Sheikha Mubarak Rashed Almansouri","corniche","3 weeks ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xwSllUTXpUblU1YkVkRWVEZFZTM05pYkMwMWFXYxAB","Michael Todd Currence","al-raha","5 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21aWlZIbElSelZEYWpaM1dsQXhVVEpuVDIxdFYwRRAB","جودي الجندي","al-raha","4 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2tVMGVISnFVMmcxZW1acWJWOWtTalp0VjA5bWMyYxAB","Soha Shami","al-raha","5 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25SYVlYa3hXSFZLY1RGS1VXbEtaVEpsTVdJME5HYxAB","Aatikah Adam","al-raha","5 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xKb2RETXhXVmgxVWpOdE0wWnpkMDl1U2xwTVFrRRAB","Nada Elsokkary","al-raha","6 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21saFpreEpRVnA0VDJwbllXTktPRGRqTkVsMlJXYxAB","Naila Rashed","al-raha","2 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pGbU9HTnNOaTFsWjFoU2FrcHRTamhGTldVNFMxRRAB","Edwina G","al-raha","3 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xwdlpXZExObXd6TVROVVlXRXlTMHRHWW5oWVIzYxAB","Louai Mohammad","al-raha","6 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT20xcU0weG5UREYzVDNsRFdUbE1SWGhsUTB0Qk5WRRAB","Ronique Britz","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25ka1RWUk9PSFZmVFROcFRIbGhTRm80Y1ROM1JHYxAB","Dr.Noushidha","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25CWGRUTlVjMmRET1RKNFZHVnZjVE5SY0RoSWQxRRAB","Iman Iman","al-raha","4 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21OWmJYcGFaV2RHWkhacVR6VlNUbDl5YTJWaVptYxAB","Razan Awad","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2sxbFZsUjZkMjUzTTJOTldYVjJhMkZ1VlRrME5VRRAB","Hamdan Alkatheeri","al-raha","5 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT201ak1XWkdNa3BYZEhONFlXMDBlVkZQVTB0RlEwRRAB","alaa al-habtari","al-raha","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnTURBNV9Db1hBEAE","Shades Beauty salon","al-raha","Edited a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2tscU5qQnZUMmgyV0hkT2REaDNaRVJqTTNwaU5sRRAB","Kristy D","al-raha","11 months ago"],
  ["ChdDSUhNMG9nS0VJM2g1WnVsOG9pZ3VRRRAB","Yazeed Abed","al-raha","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnTUNBbk5PV1lBEAE","Jackie Wilson","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2tnelJXcElOVTVQYW1wMlpDMDFNa0ZMVGtSc1oyYxAB","Jakob Serlier","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2s0eVgyMVJaR3RQWHpCSUxXWjJkVkp0WjFGUFltYxAB","E M","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2xSYWFTMUlXa0ozWlVwTldUQlFNRE5UYW1KbmMxRRAB","Ayesha Q","al-raha","a year ago"],
  ["ChZDSUhNMG9nS0VQN0t1clBQZ2J5dlN3EAE","Mahra Alm","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT25oemFrZE1aa05xWWpaR1RWUTFSRGx1ZUU5V1pHYxAB","Mohsin Ali","al-raha","a year ago"],
  ["ChZDSUhNMG9nS0VNZkJ2TFBiaVlMa1NBEAE","Nelly _dr","al-raha","a year ago"],
  ["ChZDSUhNMG9nS0VJQ0FnSUN2aWMtM0ZREAE","Bilal Nabaa","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2kxd1pUTTVNM1J3UVZwb1VtUkljRkZzWjBGdmVFRRAB","safia ahmed","al-raha","a month ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21STVRtNVhaazFWTkdKSldpMXBZbU5rTjFNdGFsRRAB","Axel","al-raha","2 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pGVFFtaG1VVTh6YmpsV05tWnpkekEwYm1OYU1GRRAB","Sanaa Freihat","al-raha","6 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2s1VVpUSjZOMVF6YzNsSFlsVjRPRE5pU2psWFkyYxAB","Sana Samhouri","al-raha","11 months ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT2pFM1lqaEdPVEV5ZERWRGFWSTRUMWxGWkU5TFgyYxAB","Mohamed Almazrouei","al-raha","a year ago"],
  ["Ci9DQUlRQUNvZENodHljRjlvT21GUlJYSktNMWhNY21ocGNUWmhUemhZT0hwM1duYxAB","Nooraldeen Kasem","al-raha","a year ago"]
]
''')

NODE_INSPECT = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const context = { window: {} };
vm.runInNewContext(fs.readFileSync(process.argv[1], "utf8"), context);
const reviews = context.window.SILWADI_GOOGLE_REVIEWS;
process.stdout.write(JSON.stringify({
  reviews,
  arrayFrozen: Object.isFrozen(reviews),
  recordsFrozen: Array.isArray(reviews) && reviews.every(Object.isFrozen),
  summariesFrozen: Array.isArray(reviews) && reviews.every(r => Object.isFrozen(r.summary))
}));
"""


class AllFiveStarReviewDataset(unittest.TestCase):
    def load_dataset(self):
        self.assertTrue(DATA_PATH.is_file(), "google-reviews-data.js must provide the verified dataset")
        result = subprocess.run(
            ["node", "-e", NODE_INSPECT, str(DATA_PATH)],
            cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return json.loads(result.stdout)

    def test_dataset_contains_all_157_unique_written_five_star_reviews(self):
        reviews = self.load_dataset()["reviews"]
        self.assertIsInstance(reviews, list)
        self.assertEqual(len(reviews), 157)
        self.assertEqual(len({review["id"] for review in reviews}), 157)
        # A fabricated/missing ID or altered Google spelling must fail, even if counts match.
        self.assertEqual(
            {(r["id"], r["reviewer"], r["branch"], r["sourceAge"]) for r in reviews},
            {tuple(identity) for identity in AUDITED_IDENTITIES},
        )

    def test_dataset_has_expected_branch_counts(self):
        reviews = self.load_dataset()["reviews"]
        self.assertEqual(Counter(r["branch"] for r in reviews), {"corniche": 126, "al-raha": 31})

    def test_dataset_has_no_empty_or_star_only_entries(self):
        for review in self.load_dataset()["reviews"]:
            with self.subTest(id=review["id"]):
                self.assertEqual(review["rating"], 5)
                self.assertTrue(review["reviewer"].strip())
                self.assertTrue(review["sourceAge"].strip())
                for language in ("en", "ar"):
                    summary = review["summary"][language].strip()
                    self.assertTrue(summary)
                    self.assertRegex(summary, r"[A-Za-z\u0600-\u06ff]")
                    self.assertIsNone(re.fullmatch(r"[\s*★☆⭐✨.،!؟…]+", summary))

    def test_every_review_has_bilingual_summary_and_branch_url(self):
        for review in self.load_dataset()["reviews"]:
            with self.subTest(id=review["id"]):
                self.assertEqual(review["sourceUrl"], BRANCH_URLS[review["branch"]])
                self.assertEqual(set(review["summary"]), {"en", "ar"})
                self.assertRegex(review["summary"]["en"], r"[A-Za-z]")
                self.assertRegex(review["summary"]["ar"], r"[\u0600-\u06ff]")
                self.assertNotEqual(review["summary"]["en"], review["summary"]["ar"])

    def test_known_same_name_records_remain_distinct_by_review_id(self):
        reviews = self.load_dataset()["reviews"]
        sanaa = [review for review in reviews if review["reviewer"] == "Sanaa Freihat"]
        self.assertEqual(
            {(r["id"], r["branch"]) for r in sanaa},
            {
                ("Ci9DQUlRQUNvZENodHljRjlvT2taNWJHWmlibGhqTWpoRFR6RmhUMVZPUTI1SlYxRRAB", "corniche"),
                ("Ci9DQUlRQUNvZENodHljRjlvT2pGVFFtaG1VVTh6YmpsV05tWnpkekEwYm1OYU1GRRAB", "al-raha"),
            },
        )
        self.assertEqual(len(sanaa), 2)
        for language in ("en", "ar"):
            self.assertNotEqual(sanaa[0]["summary"][language], sanaa[1]["summary"][language])
        waleed = [review for review in reviews if review["reviewer"] == "Waleed Humaid"]
        self.assertEqual(len(waleed), 2)
        self.assertEqual(len({review["id"] for review in waleed}), 2)

    def test_dataset_records_and_summaries_are_read_only(self):
        dataset = self.load_dataset()
        self.assertTrue(dataset["arrayFrozen"])
        self.assertTrue(dataset["recordsFrozen"])
        self.assertTrue(dataset["summariesFrozen"])


if __name__ == "__main__":
    unittest.main()
