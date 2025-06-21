echo "Comparing 2 files"
./go.sh ./test_data/csharp-warnings.before.txt   ./test_data/csharp-warnings.after.txt -o temp/csharp-warnings.txt

echo "Summarizing just 1 git-diff file"
./go.sh ./test_data/csharp-warnings.git-diff.txt -o temp/csharp-warnings.git-diff.txt
