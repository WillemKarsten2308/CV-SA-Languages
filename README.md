# SA-Languages
The aim of this project is to collect text data on South Africa's 11 official languages. English is a well documented language with a large existing text and speech database. The 10 remaining languages are severely lacking in both text and speech data. This project aims to semi-automate and simplify the process of collecting data for the various languages. This data will then be used to help [Mozilla's Common Voice Platform](https://voice.mozilla.org/) grow their database. In turn this speeds up the process of localizing the Common Voice platform to all 11 official South African languages.

## Software Setup
Before any text collection can begin a few tools and scripts are needed:
* CV Sentence Extractor
* WikiExtractor
* Rust Nightly
* Pip3  
Python3 comes preinstalled with most versions of Ubuntu.
To see if Python3 is installed on your system run the following in the terminal:
```
python3 --version
```
To install Rust run the command:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```
To install Pip3, run the command:
```
sudo apt-get update
sudo apt-get -y install python3-pip
```
To verify the install, run:
```
sudo apt-get -y install python3-pip
```
### WikiExtractor
Now, all the neccessary tools are to be installed.
First, clone WikiExtractor by running the command:
```
git clone https://github.com/attardi/wikiextractor.git
```
Now Wikipedia articles can be scraped to find sentences. A maximum of three sentences are used per article to stay within copyright regulations.
Change "en" to the language code you wish to scrape. Run the following command to obtain files and unzip them:
```
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles-multistream.xml.bz2
bzip2 -d enwiki-latest-pages-articles-multistream.xml.bz2
```
A dump can be extracted from the zip file. For this extraction JSON will be used as the output file instead of the default XML file type.
```
cd wikiextractor
git checkout e4abb4cbd019b0257824ee47c23dd163919b731b
python3 WikiExtractor.py --json ../enwiki-latest-pages-articles-multistream.xml
```
Your setup can be tested after only a few seconds of extraction. However, I recommend testing in a language you are familiar with that has a smaller database than english. Downloading and processing the English database can take hours.
### CV Sentence Extractor
Next, download the common voice sentence extractor tool:
```
git clone https://github.com/Common-Voice/cv-sentence-extractor.git
```
Before moving on I recommend reading the section on [language rules](#language-rules) and a [blocklist](#blocklist). Most languages will need custom rules, it is still worth testing with the English rules before writing new rules.
Now sentences can be scraped from the WikiExtraction files:
```
cd ../cv-sentence-extractor
pip3 install -r requirements.txt # can be skipped if your language doesn't use the Python segmenter
cargo run --release -- extract -l en -d ../wikiextractor/text/ >> wiki.en.txt
```
To scrape sentences from a break seperated file:
```
pip3 install -r requirements.txt # can be skipped if your language doesn't use the Python segmenter
cargo run --release -- extract-file -l en -d ../texts/ >> file.en.txt
```
## Language Rules
Custom rules can be defined for each language. To do this, add a <language>.toml file in the `rules` directory of the CV Sentence Extractor. Any new rules defined will overwrite the defaults when scraping sentences.
  ### Rules
  | Name   |      Description      |  Values | Default |
|--------|-----------------------|---------|---------|
| abbreviation_patterns |  Regex defining abbreviations | Rust Regex Array | all abbreviations allowed
| allowed_symbols_regex |  Regex of allowed symbols or letters. Each character gets matched against this pattern. | String Array | not used
| broken_whitespace |  Array of broken whitespaces. This could for example disallow two spaces following each other | String Array | all types of whitespaces allowed
| disallowed_symbols |  Use `allowed_symbols_regex` instead. Array of disallowed symbols or letters. Only used when allowed_symbols_regex is not set or is an empty String. | String Array | all symbols allowed
| disallowed_words |  Array of disallowed words. Prefer the blocklist approach when possible. | String Array | all words allowed
| even_symbols |  Symbols that always need an even count | Char Array | []
| matching_symbols |  Symbols that map to another | Array of matching configurations: each configuration is an Array of two values: `["match", "match"]`. See example below. | []
| max_word_count |  Maximum number of words in a sentence | integer | 14
| may_end_with_colon |  If a sentence can end with a : or not | boolean | false
| min_characters |  Minimum of character occurrences | integer | 0
| min_trimmed_length |  Minimum length of string after trimming | integer | 3
| min_word_count |  Minimum number of words in a sentence | integer | 1
| needs_letter_start |  If a sentence needs to start with a letter | boolean | true
| needs_punctuation_end |  If a sentence needs to end with a punctuation | boolean | false
| needs_uppercase_start |  If a sentence needs to start with an uppercase | boolean | false
| other_patterns |  Regex to disallow anything else | Rust Regex Array | all other patterns allowed
| quote_start_with_letter |  If a quote needs to start with a letter | boolean | true
| replacements |  Replaces abbreviations or other words according to configuration. This happens before any other rules are checked. | Array of replacement configurations: each configuration is an Array of two values: `["search", "replacement"]`. See example below. | nothing gets replaced
| segmenter |  Segmenter to use for this language. See below for more information. | "python" | using `rust-punkt` by default

  Examples for each rule implementation can be found in the [CV Sentence Extractor](https://github.com/common-voice/cv-sentence-extractor) README.
## Blocklist

## Collecting Language Statistics
  1. Scrape the entire WikiExtraction to find total sentences:
  ```
  cd ../cv-sentence-extractor
  cargo run --release -- extract -l en -d ../wikiextractor/text/ --no_check >> wiki.en.all.txt
  ```
  2. Eliminate Language Errors:  
  Run through the CTexT [Language Identifier](https://hlt.nwu.ac.za/).  
  Remove errors with Python Script.  
  ```
  python3 LID_Replace.py -c wiki.af-output.txt -i wiki.af.txt -o wiki.af.clean -l Afrikaans
  ```
  Note error percentage for file.  
  3. Count Frequency of word occurrences:
  ```
  cd  ..
  git clone https://github.com/dabinat/cvtools/
  cd cvtools
  python3 ./word_usage.py -i ../cv-sentence-extractor/wiki.en.all.txt >> word_usage.en.txt
  ```
  
  Repeat from step 2 for the text scrape that complies with the copyright lisence of your source.
  
  ## Issues Encountered
  * The Sentence Extractor will very often scrape sentences that are in the wrong language or that are broken. To fix this the resulting text file must be run through the CTexT Language Identifier. The results should be compared agaist the text file and errors should be removed.  
  
  * English rule set only allows sentences with ASCII characters, most other languages include UTF-8 characters and will thus decrease thesentence output you get. This can be fixed by writing new rules without an allowed_symbols_regex. This will default to allowing all characters. Any unwanted characters can be filtered with a disallowed_symbols rule.  
  
  * Small articles will have a massive impact on the amount of sentences that can be extracted. Articles with a very small number of sentences will result in little to no sentences being extracted from the enire article. In the case of NSO, there are thousands of articles, but after applying rules, removing errors, and following copyright restrictions we are left with only a few hundred sentences.  
  
  * When scraping with rules that are less strict, the amount of sentences will increase by a large margin. The issue is that many sentences will be added that start with non-letter characters, most ofter brackets. Making changes in the rules file will completely eliminate those sentences. The solution is to write a script to remove certain expressions, like brackets at the start of a sentence, but to keep the rest of the sentence.  
  
  * Many articles repeat the title in the text section as well. This results in repeating words and unneccesary lines. Most of these sentences can be removed by setting the minimum words per sentence to about three. However longer titles will still remain decreasing the quality of the data. Repititions can be manually removed with a script.
  
  ## Results
  ### Languages Summary  
  #### Leipzig Language Data  
  |        | Afrikaans (AFR(af)) | Sepedi (NSO(nso)) | isiZulu (ZUL(zu)) | isiXhosa (XHO(xh)) | Setswana (TSN(tn)) | Xitsonga (TSO(ts)) | Sesotho (SOT(st)) | Tshivenda (VEN(ve)) | SiSwati (SSW(ss)) | Ndebele (NBL(nr)) |
|--------|---------|--------|--------|---------|---------|---------|---------|---------|---------|---------|
|Total Number of Sentences (using no rules and no copyright limits)| 2198810 | 29819 | 401377 | 85006 | 38182 | 20541 | 20047 | 19112 | 10501 | 329 |
|Number of Usable Sentences before LID and Filtering| 1601929 | 17759 | 242394 | 58611 | 29311 | 15354 | 13604 | 14062 | 9167 | 262 |
|Number of Usable Sentences after LID and Filtering| 1599222 | 17579 | 236630 | 56761 | 27265 | 15321 | 13465 | 14042 | 9039 | 215 |
|Number of LID Errors| 2707 | 180 | 5764 | 1850 | 2066 | 33 | 139 | 20 | 128 | 47 |
|Number of sentences after 9.5 percent copyright restriction| 208887 | 2833 | 38131 | 8076 | 3627 | 1951 | 1904 | 1816 | 998 | 31 |
|Percentage Used after LID (Aim for below 10%)| 9.5% | 9.5% | 9.5% | 9.5% | 9.499% | 9.498% | 9.498% | 9.502% | 9.504 | 9.422% |
|Usable Data(Tokens)| 24984427 | 318358 | 3082119 | 783424 | 571378 | 273193 | 254775 | 245567 | 127283 | 3621 |
|Usable Data(Types)| 419136 | 21093 | 409699 | 147731 | 31487 | 22908 | 17831 | 15772 | 36811 | 2067 |
|ALL Data(Tokens)| 37350711 | 556876 | 5216871 | 1187942 | 840299 | 398591 | 428236 | 366795 | 149990 | 4615 |
|ALL Data(Types)| 529694 | 26053 | 483584 | 171900 | 37851 | 26861 | 21943 | 18747 | 40337 | 2464 |
|Average Sentence Length in Words| 15.596 | 17.926 | 12.715 | 13.366 | 19.480 | 17.792 | 18.727 | 17.463 | 13.884 | 13.820 |
|Average Sentence Length in Characters| 90.586 | 94.080 | 113.998 | 119.158 | 103.297 | 109.686 | 101.806 | 96.580 | 127.866 | 131.359 |  
  
  #### The total amount of scraped sentences per language vs Usable Sentences:
  <img src="/Images/NumSent1.png" alt="Sentences for each language" style="height: 480px; width:640px;"/>
  The ratio of total sentences to usable sentences is almost 1.  

  #### Types and Tokens Plot:
  <img src="/Images/TypesTokens1.png" alt="Types and Tokens" style="height: 480px; width:1128px;"/>
  
  #### Wikipedia Language Data  
  All data represented in the table below was acquired using the un.toml rules file unless otherwise indicated.  
|        | Afrikaans (AFR(af)) | Sepedi (NSO(nso)) | isiZulu (ZUL(zu)) | isiXhosa (XHO(xh)) | Setswana (TSN(tn)) | Xitsonga (TSO(ts)) | Sesotho (SOT(st)) | Tshivenda (VEN(ve)) | SiSwati (SSW(ss)) | Ndebele (NBL(nr)) |
|--------|---------|--------|--------|---------|---------|---------|---------|---------|---------|---------|
|Number of Articles| 103734 | 8575 | 10847 | 1436 | 867 | 740 | 994 | 716 | 588 | n/a |
|Total Number of Sentences (using no rules and no copyright limits)| 1495511 | 29036 | 55466 | 18793 | 11311 | 6659 | 7404 | 3897 | 5046 | n/a |
|Number of Usable Sentences before LID and Filtering| 79804 | 308 | 1427 | 1185 | 736 | 531 | 283 | 202 | 369 | n/a |
|Number of Usable Sentences after LID and Filtering| 79597 | 228 | 1366 | 983 | 644 | 523 | 261 | 198 | 343 | n/a |
|Number of LID Errors| 207 | 80 | 61 | 202 | 92 | 8 | 22 | 4 | 26 | n/a |
|Percentage Used after LID (Aim for below 10%)| 5.322% | 0.785% | 2.463% | 5.231% | 5.694% | 7.854% | 3.525% | 5.081% | 6.797% | n/a |
|Usable Data(Tokens)| 980003 | 3754 | 13035 | 10669 | 12676 | 7431 | 4190 | 2666 | 3649 | n/a |
|Usable Data(Types)| 76397 | 1470 | 7966 | 6560 | 2997 | 2238 | 1394 | 941 | 2474 | n/a |
|ALL Data(Tokens)| 23905740 | 254275 | 482284 | 194034 | 243235 | 100564 | 104919 | 35468 | 37491 | n/a |
|ALL Data(Types)| 542713 | 15204 | 103990 | 58393 | 19261 | 13272 | 11619 | 5306 | 15439 | n/a |
|Average Sentence Length in Words| 12.280 | 12.188 | 9.134 | 9.003 | 17.222 | 13.994 | 14.805 | 13.198 | 9.888 | n/a |
|Average Sentence Length in Characters| 76.233 | 68.247 | 83.810 | 76.759 | 92.681 | 84.586 | 82.360 | 75.312 | 88.420 | n/a |  
  #### The total amount of scraped sentences per language vs Usable Sentences:  
  <img src="/Images/NumSent.png" alt="Sentences for each language" style="height: 480px; width:640px;"/>
  The ratio of total sentences to usable sentences is very low. This is caused by copyright issues meaning that little to no sentences can be scraped from shorter articles.  
  
  #### Types and Tokens Plot:  
  <img src="/Images/TypesTokens2.png" alt="Types and Tokens" style="height: 480px; width:1128px;"/>
  
  #### Word frequency plots:  
  
  #### Compared against NCHLT text corpora:

