import requests

# URL you want to access
url = 'https://calendly.com/api/validators/slug'  # Replace with the actual URL

# Define the cookies
cookies = {
    "__cfruid": "6b9191f936f56e499556233a7fc129a88a72856b-1729596977",
    "__stripe_mid": "4111d9a8-3aef-4665-94b0-5bd8b191c4da0f5ec1",
    "_an_uid": "-1",
    "_calendly_session": "CT5/b4hmMS9AKX4/a2YyvqBG3kNYzj4QCmwkItct33/9u9l5o2YyliH7RAaPLnoUuXJpYRMLsQqyDJFWxu9Fgse84clpvHQiBlppxX47QwXkBeh9DX5U1qoIpuZqVBJOLF6V0tsr8ZPPIPKKxwEFqZXbVi+/7PxNOJfWeDYeBfmI56VMVwTurdIY+CfvtDkpCYvFwhn2wHFTft+9OMkcyisQkjBQLHgKemfE3nBUZxH5pXzdCtQUIyxBpvd1Dr4T7mbf3yFL4RQddmDtWYtVMJloJXHObc3hPX/SAUru2XfWIQS+CIdw9K7we/ONJYSXgK5faBuzKvdiyzEfC56oyzml/t/sCJIbzToHaL8IKJKsZyfGVIey8Em+/rom4x9Z9rlMgAjVKhuc7wI2qT3yFz0+z4uW4gm3zKaSq54ue+OBs19Rx61OM+i9YDVULCeX7QBcOvbNZyF0K0MZnOolAdrGjEolJ0j7IzuL5Sx6HBsuSQ7UAqyNqpNgu98O3r3xvvtqMxSRDZoxDfNqd66b7/MnuqfSsPRCBN3VP1ltp6ocywS8WXG4JvlbYdHTcuQEM+osVfKtPtW6GsPfFKwBs4RA1O76FEFUQUrqJ/BSknhinRR4nqEWECwmID+W1WtGC8UZH5ZP4dW9naRT1eHE2gXwFBy0dOG0FJyAcDo30j2csPqpN4eCl/h75creilc+LRI3W/1s2WYebndKDaSG7YfDz9SePsLWyv6gRVQvVyNl6/JSCABw0UgjAmzmcLINaPNJxdsLmiSPebxJsGzj8x0EnhC5utDIW0PpLai2nDr+GYay8r7pkdjeF9qe4zmMYTZ1ZkCzLH1xpdbepIa35pkzTlTpW/EfBwPpXr6evSBDr1rhRLPfPZLDbCdChOr6LfMRv6nW7mARoC7O5HmCM5PgGhAfvXfTfAD29cbKaXDb8H6NvC+f0VPOm0Hv0kvVG2J7pTbDSo7T6nxNzBu8jT2XKxnCFW5yx0E0UtCNAz8gWB0PMUP9PgtoPyZgXlCu+Q3JcI4aSqPQyqnlKenvqZVoJq/V94qIluzVexeeutsbOS2s5GBZpL8Cv0XO7f/rnraeLTWGBg==--xoLqrcdNX65BFo2l--CzagR0Tkp/Dr7wMy1pyzpw==",
    "_cfuvid": "XTrxKlKkyGQP2DBGW5TENR2DQ_jAz_On3renvD3Qy.Q-1729596977243-0.0.1.1-604800000",
    "_dd_s": "logs=1&id=9b4f512e-f3b1-4900-b123-88efb5bd60c5&created=1729604089648&expire=1729607645969",
    "_ga": "GA1.2.978479820.1729590959",
    "_ga_5SW884XN6D": "GS1.1.1729590958.1.0.1729590958.0.0.0",
    "_ga_DXML0NF3C7": "GS1.1.1729601435.4.1.1729601447.0.0.0",
    "_ga_HY10QQ22W2": "GS1.1.1729604501.2.1.1729604606.60.0.0",
    "_ga_V0J9YEEKGG": "GS1.2.1729604181.3.0.1729604181.0.0.0",
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
    "analytics_session_id": "1729604518787",
    "analytics_session_id.last_access": "1729604615224",
    "cb_anonymous_id": "\"b2203a0b-be21-49fc-9e18-4f5577bd51cb\"",
    "cb_group_id": "null",
    "cb_user_id": "null",
    "cf_clearance": "6rTXdZAvmoUrZ7s5XabJOoWBH1t.gXYI1r.EsMmbKgM-1729604178-1.2.1.1-8LmISZjUSK9k_GGyoCIxXQqAwLeSvpcoyRAD5mlep5UNDxiXueZofKVlweDp3zhlLGw90Zgg_Un969pvYBo3Fn.Z_pAcXaYwE6AuDvfl.BOwlOE9fJg6AigrxSlaRigvpQAlFWnsIMwwxeEfZ1pZc_IIl_XBor7ngiQmJCHrGVIU02NQFb9aUeQgXk_UP4MOp6MwZN0RYjHBtMTHfpjLSEynS_K1pGocbm9PM2FnwzJTF3OJazTy9gKDUbsTa1vtxe1GiHSw.eZDdQMePb8eTfx1uYm8iOWWZWS70D9wPj4C1WBHyquhdzrK1xI5FmOXuFVnTQXYdOWVbvpfl2Z63w",
    "country": "IN",
    "cro-variation-ids": "30158330662,6510013379248128",
    "fs_lua": "1.1729606642012",
    "fs_uid": "#rPp#3fa31cb7-cec0-45bb-bbbb-7fd24a4b57cc:a4108700-1c29-41bd-9cb6-d733cb867896:1246:0.11008434667012507",
    "fs_ua": "1",
    "frontend_cid": "625c5865c26f8c79f135c91bb9f9ebdd",
    "frontend_session_id": "06b80ca1-673f-4fbc-b582-2c01abec3b0a",
    "frontend_user_id": "17116043",
    "gtm_ua": "UA-6063589-15",
    "hsct": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ijk5OTQyMzB6ajl1NVZ4WVBPRmFTdFl3UHdZTTV2S3pJbklxcktHUVBUaHRPS0lKMDU4NmQ4a0VhbFZpNTZBODgxWUNxM2xsbDdVUU5NTm5vdjJ5V3hHRmNaYldNbnc4a3VaYXg4ZFdKZmJlYXowRVZtYlRhdTBaRzFJUlZGeXU5TVpaZzE1WmF5RHpYWE5wTDFTR0JObXV0ZyIsInRpbWUiOiIxNzI5NjA5NTA0MjQ4IiwiaWF0IjoxNzI5NjA5NTg1fQ.N8s3PlLeH-9WH20Zk3zvGHu6b5xQayF9gj56lvNNH-nNS8ThgWczNw4seGnftFydzyG6buSMtW8j9Lo0IJmN5VhI1gY0ux3Iz6pd66PbB6JH4XZf_1tS15jFUFwjDTA1v58oA-z0llH5wqafJLNqGEAL8HHhhL3bu60F71W6OFafgde5udDWCpU1z2Q3U6QUpDiCrEdJKx0H6GD_pytc90MOdZYoFOQGytcAwwJ9hKDYj7Wg31zR_5PrHzT0GscpmZNT8HZ3z5CRe0BppcU-8q7ZJlLhTw2E0I9bRqlhu-F9Pe61a1MyPtSEfOAnUIOB2F5UbQ2lZFLKnHKqj4GZpDQQ_biBWrPOhGL4I8w6LTZ2-xnml0DTCgpBf9NgAbGbPbwDZshloMsxK5_3cPfxwZ_uSwG6cRhg3_pPbPpPRw2NMOee8TtWb8_VzGZ6AlOZss9obPf6WR8VczX1InYcZXG60uM2lOMkvPCt-K2QntmI7H2CzYg2r28ydbf1G53GOQXS82MTv7r51KOBxD3T3Tb7G3X3PRvK-hrDK5YoRVw3kSTtkP7Tu1oOcDN8SKlXbhtTT9m5m_VXiRM6HDWOLW1X4CwH0heBSbUm98ZBLThcTwtfwiT5CB-PLMIYhHz13uhFZfs6K-WY2X0_0G4k77bbfJ_oPMLL1DSr6VeF6ndHewpFW4zls8hD3zHl5k9bcHHoiW8_4S2Q3w6gdxab6xCgtFO3vwxw4FsGmNkBtf0WZ6x04zSoJvWtoOxD9voBUB9P7DHoC1qU7EGyH1MXSz3MNwgsPxBXQUGFG4w0--L1H-0mITNTH-pN4yfKCNJcYqG96lRSzyT0gq1DNwAqyyijqLZg",
    "is_ac": "1",
    "is_connected": "true",
    "is_subscribed": "1",
    "kol_tmt": "0",
    "last_visit": "1729604761588",
    "session_id": "aa59472f-b4ea-476b-a80a-c55a8d3e0a7a",
    "session_token": "f8fcb4d8-9d60-4383-b4cd-d6cf89e12104",
    "tktc": "1",
    "upscope__email": "manaslaud2004@gmail.com",
    "upscope__name": "Manas Laud",
    "upscope__time": "1698451364420",
    "user_id": "17116043",
    "visit_id": "1729596391444"
}

# Define the headers
trick_header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0'
}

# Send a GET request with the cookies and headers
response = requests.get(url, cookies=cookies, headers=trick_header)

# Print the response text (or handle it as needed)
print(response.text)
