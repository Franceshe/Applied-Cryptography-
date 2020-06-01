# MP4

The Pretty Bad Privacy (PBP) encryption tool can be used to insecurely encrypt files to a 2048-bit RSA public key using 128-bit AES.

Checked into the gitlab repository above is a PDF file that has been encrypted using PBP to the following RSA public key:

```
$ cat key.pub
-----BEGIN PUBLIC KEY-----
MIIBIDANBgkqhkiG9w0BAQEFAAOCAQ0AMIIBCAKCAQEA0KkIEANhLwe2cU9e+rrW
8f2zAyK95+ky8+hUj6NO4RD8zKAxGx3J0C92DcSI33vhpTo8O4yToP3+zhuDOPjO
cLwSICmo0YZ+vCmDiZ6jihJ/H94ibNuyEQsbpb5pGnPzyEl7wAhTlHtJyBwtHQjF
NqIS9DVIlDDGqvjfP2xluxh4RdYlezQoIbObiLDnIDr/kdJfDC27rc4vrnKoxZsb
Bo8p7nrrKEckj1zCOo5+WJ7leDPZeKOwLfz1NURwZwQ2fqgOwmDnWLctLfh0ieiQ
lZHgYJIsHSp3GZjhyFWx/wZMA6YYSayyoXOPueCCrv/f20kiM2gsBF3+wVTY91l2
6QIBAw==
-----END PUBLIC KEY-----
```

# Running Instructions:

You will need to install docker to run this assignment. Docker CE(Community Edition) is supported on both Windows and Linux machines. 

```
docker pull sagemath/sagemath:develop-py3
docker run -it -v $PWD:/home/sage/mp4/ --name sage sagemath/sagemath:develop-py3 bash
pip3 install pycrypto # inside the container
```
Please ask questions on piazza if you are struggling to setup for the assignment. It is recommeneded to start the assignment early to aviod last minute installation related questions.

# Instructions

Your task is to break the RSA-encrypted AES symmetric key, and use it to decrypt the attached file. Fortunately for you, PBP designed its own padding scheme.
 
The exact code used to encrypt the file, `pbp.py`, is also found in the repo. You will want to start by knowing how to generate keys and run that code yourself. The following commands are how the keys were originally generated:

```bash
openssl genrsa -3 -out key.pem 2048

openssl rsa -in key.pem -outform PEM -pubout -out key.pub
```
 

You will probably want to use an implementation of the LLL algorithm. Sage's documentation for that function is [here](http://doc.sagemath.org/html/en/reference/matrices/sage/matrix/matrix_integer_dense.html) and documentation on polynomial construction and root-finding is [here](http://doc.sagemath.org/html/en/constructions/polynomials.html).

The found the following sets of slides very helpful for understanding Coppersmith's attacks on RSA.

- Slides on Coppersmith attacks from Nadia Heninger (http://attackschool.di.uminho.pt/slides/slides_nh4.pdf)

- http://www.untruth.org/~josh/school/phd/seminar/fall-2010-coppersmiths-theorem/coppersmiths-theorem-combined.pdf

- http://www-polsys.lip6.fr/~renault/CryptoM2/PDF/Intro-Coppersmith.pdf

 

This paper from Alexander May has the clearest and most complete technical explanation of the technique and its underlying theory.

http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.86.9408&rep=rep1&type=pdf

  

The following set of python code is also useful and comes with some helpful explanations. You are welcome to use this code as a starting point to solve the problem:

https://github.com/mimoo/RSA-and-LLL-attacks

  

What to submit:

- Make a private piazza post by 11:59pm, Nov 19th

- The post should include an attachment of a single .sage or .py file that you used to decrypt the file

- As usual, please include a text file report.txt that describes what steps you took, what resources you used and/or found helpful.

- In your report.txt, include the text of the message contained within the decrypted PDF

- You may discuss this assignment in small groups with classmates, but please code and write up your solutions yourself. Please credit any collaborators you discussed with and any references you used in the report.txt