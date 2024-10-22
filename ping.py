import requests
from bs4 import BeautifulSoup
import json
# URL you want to access
url = 'https://calendly.com/api/validators/slug'  # Replace with the actual URL

# Define the cookies
cookies = {
    "__cfruid": "6b9191f936f56e499556233a7fc129a88a72856b-1729596977",
    "__stripe_mid": "4111d9a8-3aef-4665-94b0-5bd8b191c4da0f5ec1",
    "_an_uid": "-1",
    "_calendly_session": "MT/HuB5igSaa01VO4K5tjubuDKuDbagkDpG1C7dUsDW8sT201KalomDOWca099mTksxINTmscpD7Jh/yg4DM6O6HFtD3TNr7q33o+H9RIudHc8OWwn375eF93QhjGZp16OXIuFqunlqpSQj4DSyCJwSoF+2Ot4jBY75Vcx05Rs/Uhofl2H8lj6EIsiU+YIIgNkRAnN57BZFxoj4Kw5bFbiogEVrSGyUyb3Kzn+3Mn/YVZH6cuJNU9MNhHbSvNgqp9BW4QwsdBbuBgp4Yai6f8cUtI5rUZqCdAyYDO8/qshjySyaVhwNJRPwNQJlKrGfVnVT1fUckY/4QBeQryGrrDdo3J/yz8VLTFNn4bIjssdmJqHse7toigO3bB65zPCnp15cg8OvfHvGUaLOX4LWFTlofjdnH8B6GpcXj9siT0rrc2s4MEyJTwowHIx0YxHi+Nkayfl5dORWv9aIzccuXXBvHIZ+Km1gn3F+cFdr6nrUs4790MRl1Edt3K2ydw0Fb/3EWgj3VaprItR/Q15Yj1Rbjj4VnJs44pqci6ZeIA2wyB9zSzfahS0Fpz01/xhi1N5P399hq+F+C169jMlUi1rmMGEjbyau0U0/2VzsO+1ZGVDaLgdybvLEJkwV0jiSjBXWTW0jk2PDCsrIfOwIdHTmKwyE6pb1+fIXSszDJqAXTl5Ufj5n7x7KUfzxd8Sg5v4ODl3W3iR3/SyuzGXrh4d63cCHQN/iv7GZRoAUgnCMtneYg8rkN46pPbduDorwrQidZzm6B2hv3oBTq5fS9Lmc9wS4IEsJ0NW2T+CuXZRC9DksqLu7zw2LLoP/S4HhHJKI49wDi4bhuSjPSRHqu5UZY5GvlklqJe0s06+m8TgbFTcFU+MCZkcjpVBxle641SKu5Affg+cIpXa/g7rDx2MWhd+IaRUHjeojE/+4sOT5+BmY41EGSKO2/W4hl3mrzTw2vKKccNFrIti8+EWwBISUmSqGYgNTHNWy0sMw+UEN51ZnRlAsJO5W7NFqHhnynedUAfU+kXDk2t/I=--g9I0mk5QbBnDKrzZ--pYYLpuBGfyqNGv14mZFw9w==",
    "_cfuvid": "XTrxKlKkyGQP2DBGW5TENR2DQ_jAz_On3renvD3Qy.Q-1729596977243-0.0.1.1-604800000",
    "_dd_s": "logs=1&id=9b4f512e-f3b1-4900-b123-88efb5bd60c5&created=1729604089648&expire=1729610728952",
    "_ga": "GA1.2.978479820.1729590959",
    "_ga_5SW884XN6D": "GS1.1.1729590958.1.0.1729590958.0.0.0",
    "_ga_DXML0NF3C7": "GS1.1.1729601435.4.1.1729601447.0.0.0",
    "_ga_HY10QQ22W2": "GS1.1.1729609642.3.1.1729609812.54.0.0",
    "_ga_V0J9YEEKGG": "GS1.2.1729609490.4.0.1729609490.0.0.0",
    "_gat_UA-42305411-1": "1",
    "_gcl_au": "1.1.1688742481.1729597149",
    "_gd_session": "b08cb974-c331-4c63-8fb8-e58899d3cf42",
    "_gd_visitor": "3fd83c95-c5f2-4441-88eb-9d05db0e9e86",
    "_gid": "GA1.2.1566938549.1729590960",
    "_mkto_trk": "id:482-NMZ-854&token:_mch-calendly.com-1729597152224-80017",
    "_rdt_uuid": "1729597151481.45e7b0d3-8ebb-441b-8eed-0fb772cc6de3",
    "_uetsid": "422d7080906a11ef878a99c11071ea29",
    "_uetvid": "422d86c0906a11ef892f0d6e55d11218",
    "_upscope__region": "ImFwLXNvdXRoZWFzdCI=",
    "_upscope__shortId": "IllSTlNRWFlGNTNLTVRZUlhZIg==",
    "ajs_anonymous_id": "b8538b6e-f882-45f3-9424-40f38b3bd14e",
    "ajs_group_id": "39019248",
    "ajs_user_id": "39042174",
    "analytics_session_id": "1729609625299",
    "analytics_session_id.last_access": "1729609823982",
    "cb_anonymous_id": "\"b2203a0b-be21-49fc-9e18-4f5577bd51cb\"",
    "cb_group_id": "null",
    "cb_user_id": "null",
    "cf_clearance": "NobyMcVSiySOdvixBhnhR7gPrPoywySbIGPFBcV0gwU-1729609488-1.2.1.1-RM7pumZcOEOgcmWSvGqXY2.iPrqwFwEqWB5yh_fWFnzalWiZf3Zy0XxBpy.9xgOOBBfvQYuntzYgMnWjBTswt80F.pD1bMPCuLZMp1TOSk1M3Z6l8fGSU9kCe1MwhhxzwYA4.azlQXZrEqQ50jNVa3DKG_FQxRX79_mZjkv1gW88_PrNlS5ecc71HU6TyByk0EjjEJWHPULQCix.d6Al0Hixd_WATaWQCHtj7X4Wky64NjO7obVVRVgtEaNEnA3uUTfuw7IjoO_rurEafQvcDT63px_9159Q3jhb8FUHItjS286qOlSwlODvWqYxeK.n0Pd2sbhNW03gd5HW3Ne5r43afykmtlM3v5k.ljwJZPzT.R9wnyOR5JgB4SMsezAnBZ_t9yU7TX31oNIMU6Tt8e2OcYtD35oOUF0-1nscHCSKm5G1BdMtfGHjYUv8bUBWjNyYm0MfmEV0NK21PhWIS-7k8mnIk_fX7n5PSM3G_oSMp3__oMOzr6tL8Y7J-8dSeMN0o2dhTovMcbfIF8OlFP-4WYYE2gM8R7MeXHqADZwPi7De2VkBSgG0dhrRr1b2CrK_98iZSLkZCHQR3cIYuyR3JcUVcC9wTpeGr1oa0Z4TPgi-18lEvBqWUsH4uv7VeDqcmCOekacP8rHyA3DB9CKu6C-1Neqoa8wVSBZFBHPMHR5cO3BVDfKfSlM.IcHTlU5KSR8LVwFSmQG5ynhrf7UsQCK73hl_s.sC05C6wHMAhGJBRsYmC4.6tQKDxr6W3Lwco6b3CInXg..3qUnVgMtiOBYZjMQcqW3EB4hMdsBI2OY7pdRNRy7h_3pn5EXsFQG8qY.KsT3AZ19v10nG1wnb6U9gE2aG35ZtbSRDgPtTp0BPxHMJkp_EFBFL5pHwlFvLz8f2u0Q7McziYOV7nG_D_ovunJsP0_Xy9jnt8-0IGGp36Mr3f8.z0OeiENh4lV_xl9GHtOENZFxNTz2iBY3y_gE-3EFts0GN4ch18rYw7jYctjZmfkOEw5YlYXOMocA.hI7AhWg2Vt8e4Hpm7VfuP-CbAxRoqTYg0cMzVBqbeB9SO5HhcfwEYdMzxInJER82GM88BOmgnFjPLOoYqstg28DOpK1cdD9ZdLtMO_dRG9obY1y64j2COlo8uh9KXo1Hek6GNcDBCMnt_2C8tDNYN1NE8dpYUsnZK7AuVxhiWkH5aXPKi6XvbdRM_D8cXq2QCDXL96FnbcG2-6YbU0I5Da4vxU0BZVxBzJuNENva3oz6Uw9LFwVrt1V1B1_Lg3QWnhNdT3w_DH6Ey9kFY8W8E3_q8f34IzHn-6W_1AfJ4HzprM0nDTzEx0Lt2R39j8.vgoUKH7h_S90Qz9vlwAvmopEJff9LDNZMS43QRUtnf03e4_gwiHiVb1l8C20MNhAFw6h5BmfTcyuOlj1Ic8epA0D1RthRBGZ8GbY8pA_NhMCFIk6NYGgsdvnP3KgrBeH4dUuPGgj3zJlO9WWOewqneGiZT24_ZvHnJ8UUG3fG7IQ3f9m93ujd2Hg3zEEl9f31y-0OtjYbftgRNs9zM4l2RaHDmbuvVhF_D3nUmp0BPG6ZrfvH8CyG1iN63D56fUuufmR7xMPcRmZNNJljytMn4zDQNa3tRSKowNq2DIsW38PcfXUtyy0JpmV4VAlxTfXU8ShHSHG1tYYLe6wzHUszEG1QZgb0IPqCzgq33fKKkLwDq4bJHf9ByF9KcSN5I4ZZ2Lp1CqGWkY6OjYO6pHeNwznQ6c5J1evJkUUXk9BhPcXLFFpLj5Q8kDrGFLiIX2a5CtzvEPmpkwzBMSMWMIeZnFQuUp7GxiSVqQxfqIoZmYy0nG1HmkUGDGLZhg64p2F4A7rSmytNFctN6-5E60nWgVs_nVNU5LtYjHhDEtmY7HS82x7EYhtE6HjqbwV4K7IuKKhDwj52OAIU3PbPAReRZYfaLfAK8TTnEUC6_bCudHP2oV8lRfNWu2I9H6CeIOfv8jsAe7ZcDh8PI9p_16sSQNGuRU_O58yevaQZsRiOi0G7iWGEHSLxKu4cZcL_WXSNEfkp27CxtlEabmbCDoLL9Qp7BB9WhKiYGGVspK8HWgX34_lj5z_09gdFVmQLa80DYOX0FNvTVRA55GgLx2u0D4a21ftRxnK0D5F5Q_AvOfr16bxgWAPXE0OHGuItmlg1S5gRz95zE4UlLo3RxX6auuT4Sw8ybEHP2y4W69Rve8dtLsyG5gnDBH50rP2gv6zbdpB_W1pFeQVmj5hS5m6Q9H1byWT0XNSDMym5CIzLL0CckX9HDC6CX4DSzKFmQU76UQ6T3VvRM9jbVAsUQya1WMIiNgj2mJx2voOe_VzpTMsTGBb_h6HtsBQmszYwRj5z5N0RF1QUzQgoWw34jzCwoHo6F5UimDMz4f93Q2PVYNxkslPwiWQLgmWqU2XGpUExK_9W0NQ1HhqsZJIXUExR4sbV75Ke8T8N2zPnvZ1FS7wShbM1HrOxlU6wAXqC67wBiB8M4dpLtDGAAB-_5I=--UorL8EjYywS8tWbe--nYlU1D7TZp7Rj8ufwME7hw=="
}



# Define the headers
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Content-Length': '53',
    'Content-Type': 'application/json',
    'Host': 'calendly.com',
    'Origin': 'https://calendly.com',
    'Referer': 'https://calendly.com/app/personal/link',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE': 'trailers',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'X-CSRF-Token': '-R6lZZPVJYyPreAXqKccH29HPEv8_aZjzg464Gah_iarr6YZEZ3Tth-9_1HKkxD-1OIwLy1OP_oDHzjSYayBLg',
    'X-Page-Rendered-At': 'null',
    'X-Requested-With': 'XMLHttpRequest'
}


# Send a GET request with the cookies and headers
payload=json.dumps({"slug":"ma","owner_id":39042174,"owner_type":"User"})

response = requests.post(url, cookies=cookies, headers=headers,data=payload)
# Print the response text (or handle it as needed)
# print(response.text)
soup = BeautifulSoup(response.text, 'lxml')

# Print the prettified HTML or extract specific content
print(soup.prettify())  # This prints the entire HTML in a readable format

# Optionally, extract specific elements
# For example, to find all <h1> tags:
h1_tags = soup.find_all('h1')
for tag in h1_tags:
    print(tag.get_text())

