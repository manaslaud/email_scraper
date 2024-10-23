const sendRequest = async () => {
    const url = "https://calendly.com/api/validators/slug"; // Replace with your URL
    const payload ={"slug":"manaslaud","owner_id":39042174,"owner_type":"User"};

    const cookies = [
        "__cfruid=6b9191f936f56e499556233a7fc129a88a72856b-1729596977",
        "__stripe_mid=4111d9a8-3aef-4665-94b0-5bd8b191c4da0f5ec1",
        "_an_uid=-1",
        "_calendly_session=lyVIjZw4PIK46RjQvOrTQj1iFVxNLJWG49OBSmMIJ7AF7+4JMBYFgMLIqYOcCJHSN8++MnM8d2a6lMz6gm0/FMHlatE6e4rpMU0Ki6ihQb7+w0qNhJz+MSwEDURuPeAITIqIlQDTCJlG+Vw9Pz2FPKKCA1BFMKO5KeZp6erVO9aYblx5KqK1tsO+iGqY+MrKj5J43gcZ+pfexKGX2F3+ljVRk5F9oPUGKj4HgaX8zx5Rjgi7eKUvgYt/+CHAqzdpz+wrT2x3oQVd5NuOmFrxNMsKS5gZclrRodglnpFHHObwIR8zrsOKK9ihFYLtiSxGG1Bw2fDp3KjniG396Ou9+jlRISOSDhyL89J6hyVWu6kEjAltk/AiEtGxsGFh1SiOWiQ32NliGlNE4L0oBHixcYRez7g00gghwYV06DsmBo4ukyDKtV7Cmuoq8pGjSvW/22Dgc54asFAc3GfPfi/dJgYqcTEpQaxofcC7st2VXlluFvfOMk1x1vJ/2bkwUnLosczMqPGy4413FQViW2xtwOEsgWvw67KGMlc5VltArg67yGoLISp355O1/G+z1C1GcuGWxQixegHg+3lMz56by5JuAydMGlA3b3dWNPlJpoXnNvYZsy50OmSfILDSIMPxNZf+KxUAZpHbmaIZd+VDYH0lZm+97hEhub6MmkMTJ9x/QnIk95A0K3VIaqUUivN+CimC7+7at4NGizXe7K7fqGk1LR/PyZUBKa4lHXYB+ZuACzbqJCYlp1VRZnNmNO0s/+h9YbOHWsjf2BKWqnYGl8rwn8EeCaUWl3dlqEt3QQENPzNNWyPS+Ailb/ZL4ajRKxCHAHbrl67csw4mGcAoWG0wIY6lxn+ILwNGf/rm+U0bNnywu6pXECpO3l0HqS+n0KyhsA4fly4wji03ecG1kYqQvExMjsgNwhsISRnWAMMN/La64JA+y9ga7RK8dTo1EKumZ5ivY/5zSIWpHeqRwoUNUr9FCQ0rkcdbBKOwj1r+Bttdw6pCyrZN4p7/v6ISUDu33Tnm+zh8XgvifnNbgYbIjvsd6d/hkpo9+561+ePoK5VlnkOSQ8DBRgufl3SeDKi20wIWlw==--wAL1mFzDn6GeXY0k--JffPI7Cv6+JfhLXw7jVM6g==",
        "_cfuvid=XTrxKlKkyGQP2DBGW5TENR2DQ_jAz_On3renvD3Qy.Q-1729596977243-0.0.1.1-604800000",
        "_dd_s=logs=1&id=9b4f512e-f3b1-4900-b123-88efb5bd60c5&created=1729604089648&expire=1729608571637",
        "_ga=GA1.2.978479820.1729590959",
        "_ga_5SW884XN6D=GS1.1.1729590958.1.0.1729590958.0.0.0",
        "_ga_DXML0NF3C7=GS1.1.1729601435.4.1.1729601447.0.0.0",
        "_ga_HY10QQ22W2=GS1.1.1729604501.2.1.1729604606.60.0.0",
        "_ga_V0J9YEEKGG=GS1.2.1729604181.3.0.1729604181.0.0.0",
        "_gcl_au=1.1.1688742481.1729597149",
        "_gd_session=b08cb974-c331-4c63-8fb8-e58899d3cf42",
        "_gd_visitor=3fd83c95-c5f2-4441-88eb-9d05db0e9e86",
        "_gid=GA1.2.1566938549.1729590960",
        "_mkto_trk=id:482-NMZ-854&token:_mch-calendly.com-1729597152224-80017",
        "_rdt_uuid=1729597151481.45e7b0d3-8ebb-441b-8eed-0fb772cc6de3",
        "_uetsid=422d7080906a11ef878a99c11071ea29",
        "_uetvid=422d86c0906a11ef892f0d6e55d11218",
        "_upscope__region=ImFwLXNvdXRoZWFzdCI=",
        "_upscope__shortId=IllSTlNRWFlGNTNLTVRZUlhZIg==",
        "ajs_anonymous_id=b8538b6e-f882-45f3-9424-40f38b3bd14e",
        "ajs_group_id=39019248",
        "ajs_user_id=39042174",
        "analytics_session_id=1729606828814",
        "analytics_session_id.last_access=1729606830460",
        "cb_anonymous_id=\"b2203a0b-be21-49fc-9e18-4f5577bd51cb\"",
        "cb_group_id=null",
        "cb_user_id=null",
        "cf_clearance=6rTXdZAvmoUrZ7s5XabJOoWBH1t.gXYI1r.EsMmbKgM-1729604178-1.2.1.1-8LmISZjUSK9k_GGyoCIxXQqAwLeSvpcoyRAD5mlep5UNDxiXueZofKVlweDp3zhlLGw90Zgg_Un969pvYBo3Fn.Z_pAcXaYwE6AuDvfl.BOwlOE9fJg6AigrxSlaRigvpQAlFWnsIMwwxeEfZ1pZc_IIl_XBor7ngiQmJCHrGVIU02NQFb9aUeQgXk_UP4MOp6MwZN0RYjHBtMTHfpjLSEynS_K1pGocbm9PM2FnwzJTF3OJazTy9gKDUbsTa1vtxe1GiHSw.eZDdQMePb8eTfx1uYm8iOWWZWS70D9wPj4C1WBHyquhdzrK1xI5FmOXuFVnTQXYdOWVbvpfl2Z63w",
        "country=IN",
        "cro-variation-ids=30158330662,6510013379248128",
        "fs_lua=1.1729606827875",
        "fs_uid=#rPp#3fa31cb7-cec0-45bb-bbbb-7fd24a4b57cc:a4108700-1c29-41bd-9cb6-8c2f12af4b47:1729597151727::11#fa72a73f#/1761133180",
        "gsg_encountered=true",
        "OptanonAlertBoxClosed=2024-10-22T11:36:22.884Z",
        "OptanonConsent=isGpcEnabled=0&datestamp=Tue+Oct+22+2024+19:13:33+GMT+0530+(India+Standard+Time)&version=202403.1.0&browserGpcFlag=0&consentId=0d78756d-b7cb-4401-bb3c-c0e3c35f81f3&interactionCount=1&landingPath=https%3A%2F%2Fcalendly.com%2F&groups=220af663-d3c1-43d3-8a36-24d17d58f4f0%3A1%2C59954b26-e81f-4870-bfd0-d3c573ed7b41%3A1%2C5f580cd3-22b5-4344-8357-7d7f1a1fa5a3%3A1%2C0b34f4c8-dbb0-420f-9fa0-07f0fd3fda9c%3A1%2C49c9a205-d70b-4a3e-bb66-df593b3eb0c1%3A1&awaitingUpdate=0",
        "session_id=6366e83c-1323-45d7-9118-16b3e61b4c5c",
        "uid=11673267"
    ];
    
    const cookieHeader = cookies.join('; ');    

    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',
            "Cookie": cookieHeader, // Add the cookies header (currently empty)
            // Add any additional headers if needed
        },
        body: JSON.stringify(payload),
        credentials: "include", // This ensures cookies are sent
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
};

sendRequest()
    .then((data) => console.log(data))
    .catch((error) => console.error('Error:', error));
