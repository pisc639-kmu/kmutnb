import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://reg.kmutnb.ac.th/',
    'Content-Type': 'application/json',
    'Content-Encoding': 'gzip',
    'Authorization': 'Bearer eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IuC4nuC4teC4o-C4nuC4h-C4qOC5jCIsInVzZXJuYW1lZW5nIjoiUEVFUkFQT05HIiwic2Vzc2lvbiI6ImVjdXdNOTRLdGRpdVYzbG9RVFlJL2c9PSIsInJvbGUiOlsic3R1ZGVudCIsIiJdLCJuYmYiOjE3NTkyMTQ2MzYsImV4cCI6MTc1OTIxODIzNiwiaWF0IjoxNzU5MjE0NjM2fQ.bXdCEHedd0nhgBDi6HSkhh2fyGCa5xsIRGOukpNQPc3FXjEd_2SqBfR5bTN_qWEcjBS7WArNZRUdAQZcnEXHxA',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

response = requests.get('https://reg.kmutnb.ac.th/regapiweb1/api/en/Validate/Token', headers=headers)
print(response.reason)
print(response.text)
if __name__ == "__main__":
    while True:
        try:
            command = input(">>> ")
            if command == "exit": break
            try:
                print(eval(command))
            except SyntaxError:
                try:
                    exec(command)
                except:
                    import traceback
                    traceback.print_exc()
            except:
                import traceback
                traceback.print_exc()
        except KeyboardInterrupt:
            # print("^C")
            print("\nKeyboardInterrupt")
        except EOFError:
            print("")
            break