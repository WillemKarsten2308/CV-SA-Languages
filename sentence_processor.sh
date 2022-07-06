lang=$1
rules=$2

# sudo apt install subversion

mkdir Out_$1
cd Out_$1

git clone https://github.com/Common-Voice/cv-sentence-extractor.git
git clone https://github.com/attardi/wikiextractor.git

cp ../Custom_Rules/$2.toml cv-sentence-extractor/src/rules/$2.toml

# mkdir saScripts
# cd saScripts
# svn checkout https://github.com/WillemKarsten2308/SA-Languages/trunk/Scripts
# cd ../

wget https://dumps.wikimedia.org/$1wiki/latest/$1wiki-latest-pages-articles-multistream.xml.bz2
bzip2 -d $1wiki-latest-pages-articles-multistream.xml.bz2

cd wikiextractor
git checkout e4abb4cbd019b0257824ee47c23dd163919b731b
python3 WikiExtractor.py --json ../$1wiki-latest-pages-articles-multistream.xml

cd ../cv-sentence-extractor
pip3 install -r requirements.txt # can be skipped if your language doesn't use the Python segmenter
cargo run --release -- extract -l $2 -d ../wikiextractor/text/ >> wiki.$1.txt
cargo run --release -- extract -l $2 -d ../wikiextractor/text/ --no_check >> wiki.$1.all.txt

cd  ..
git clone https://github.com/dabinat/cvtools/
cd cvtools
python3 ./word_usage.py -i ../cv-sentence-extractor/wiki.$1.txt >> word_usage.$1.txt
python3 ./word_usage.py -i ../cv-sentence-extractor/wiki.$1.all.txt >> word_usage.$1.all.txt

cd ../
wget https://repo.sadilar.org/bitstream/handle/20.500.12185/350/nchlt_south_african_language_identifier_v.1.0..zip;isAllowed=y
unzip nchlt_south_african_language_identifier_v.1.0..zip

cd "NCHLT South African Language Identifier"/linux
cp ../../cv-sentence-extractor/wiki.$1.txt wiki.$1.txt

chmod +x ./salid
./salid id -i ./wiki.$1.txt -l -o ./lidResult_$1

cd ../
cd ../cv-sentence-extractor

# Save stats to file named Stats_$1.txt
printf "Statistics of $1\n\n" > Stats_$1.txt

printf "Sentence length in Characters: " >> Stats_$1.txt
python3 ../../char_counter.py -l wiki.$1.txt | tee -a Stats_$1.txt

printf "Tokens in Usable (Total words): " >> Stats_$1.txt
wCount=($(wc -w < wiki.$1.txt))
echo $wCount | tee -a Stats_$1.txt

printf "Number of usable sentences before LID and Filtering: " >> Stats_$1.txt
sCount=($(wc -l < wiki.$1.txt))
echo $sCount | tee -a Stats_$1.txt

printf "Number of usable sentences after LID and Filtering: " >> Stats_$1.txt
aCount=($(wc -l < ../"NCHLT South African Language Identifier"/linux/lidResult_$1/$1.wiki.$1.txt))
echo $aCount | tee -a Stats_$1.txt

printf "Number of LID errors: " >> Stats_$1.txt
echo "scale=1 ; $sCount - $aCount" | bc | tee -a Stats_$1.txt

printf "Total Sentences before LID and Filtering (ALL): " >> Stats_$1.txt
fCount=($(wc -l < wiki.$1.all.txt))
echo $fCount | tee -a Stats_$1.txt

printf "Percentage used after LID: " >> Stats_$1.txt
echo "scale=6 ; $aCount / $fCount" | bc | tee -a Stats_$1.txt

printf "Average sentence length in Words: " >> Stats_$1.txt
echo "scale=3 ; $wCount / $sCount" | bc | tee -a Stats_$1.txt

printf "Types in Usable (Different): " >> Stats_$1.txt
wc -l < ../cvtools/word_usage.$1.txt | tee -a Stats_$1.txt

printf "Tokens of ALL: " >> Stats_$1.txt
wc -w < wiki.$1.all.txt | tee -a Stats_$1.txt

printf "Types of ALL: " >> Stats_$1.txt
wc -l < ../cvtools/word_usage.$1.all.txt | tee -a Stats_$1.txt

printf "Number of Articles: " >> Stats_$1.txt
cat ../wikiextractor/text/AA/* > ALL1.txt
cat ../wikiextractor/text/AB/* > ALL2.txt
# cat ../wikiextractor/text/AC/* > ALL3.txt
cat ALL*.txt >> FinalAll.txt
wc -l < FinalAll.txt | tee -a Stats_$1.txt

printf "\nEND OF FILE\n" >> Stats_$1.txt

