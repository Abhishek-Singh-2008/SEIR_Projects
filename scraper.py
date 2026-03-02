import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# It will take URL from command line
if len(sys.argv)==2:

  url = sys.argv[1]
  if not url.startswith("http"):
    url="https://"+url

  response = requests.get(url)

  # It will create soup of texts using html parser
  soup = BeautifulSoup(response.text, "html.parser")

  print(f"PAGE TITLE WITHOUT ANY HTML TAG:{soup.title.text} \n")
  print()

  print("PAGE BODY TEXT IN LOWERCASE:")
  Sentence_Body=(soup.get_text()).split()
  Sentence_Body_lowercase=[]
  for i in Sentence_Body:
    Sentence_Body_lowercase.append(i.lower())
  print(Sentence_Body_lowercase)
  print()
  print()
  print()

  print("ALL THE URLS THAT THE PAGE POINTS TO: \n")

  for link in soup.find_all("a"):
      href = link.get("href")
      
      if href:
          full_url = urljoin(url, href)
          print(full_url)



elif len(sys.argv) == 3:

  url = sys.argv[2]
  # if not url.startswith("http"):
  #   url="https://"+url
  def Simhash_code(urls):
    response = requests.get(urls)
    soup = BeautifulSoup(response.text, "html.parser")

    
    print("PAGE TITLE: \n")
    print(soup.title.string)
    print()

    print("PAGE BODY: a word is a sequence of alphanumeric characters, case does NOT matter \n")
    Sentence_Body=(soup.get_text()).split()
    Sentence_Body_lowercase=[]
    stopwords = {"the","is","am","are","was","were","and","of","to","in","on","for","with","a","an","that","this","it"}  
    for i in Sentence_Body:
      if i.isalnum() and i not in stopwords:
        Sentence_Body_lowercase.append(i.lower())


    print("Printing words and their respective weights of the document \n")
    word_dict={}
    for i in Sentence_Body_lowercase:
      word_dict[i] = word_dict.get(i, 0)+1
    print(word_dict)

    print()

    def Binary_64(num):
      binary = ""
      n = num
      while n > 0:
          remainder = n % 2
          binary = str(remainder) + binary
          n = n // 2

      while len(binary) < 64:
          binary = "0" + binary   # Adding zero at first to make it 64 bit 
      return binary


    print()
    print("64 bit Hash Values for each word using polynomial rolling hash function \n")
    def Polynomial_hash(Sentence_Body):  #Created function to generate HashValues of each word
      p = 53
      m = 2**64

      hash_values=[]
      for wrd in Sentence_Body:
          hash_value = 0
          power = 0
          for w in wrd:
            ascii_value = ord(w)     
            hash_value = (hash_value + ascii_value * (p**power)) % m 
            power+=1
          hash_values.append(Binary_64(hash_value))

      print( hash_values)          
      return hash_values
    hash_values=Polynomial_hash(Sentence_Body_lowercase)

    print()
    print("64 bit Vector formed by summing weights \n")
    words = list(word_dict.values())
    # print(f"words :{words}")
    arr=[0]*64
    for i in range(len(words)):
      for j in range(64):
        if (hash_values[i][j]=='0'):
          arr[j]-=words[i]
        else:
          arr[j]+=words[i]
    print(arr)

    print()

    print("Final 64 bit hashcode of the document \n")
    for i in range(64):
      if (arr[i]<=0):
        arr[i]=0
      else:
        arr[i]=1
    print(arr)
    return arr
  print()
  print()
  url1=sys.argv[1]
  if not url1.startswith("http"):
    url1="https://"+url1
  
  url2=sys.argv[2]
  if not url2.startswith("http"):
    url2="https://"+url2
  hashcode_1=Simhash_code(url1)
  print()
  hashcode_2=Simhash_code(url2)
  print()
  print(f"This is the HashCode of documet 1:{hashcode_1} \n")

  print(f"This is the HashCode of document 2:{hashcode_2} \n")
  print()
  count=0
  for i in range(64):
    if hashcode_1[i]==hashcode_2[i]:
      count+=1
  print(f"                       {count} bits are common in given two documents")