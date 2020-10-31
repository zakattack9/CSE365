#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <map>
#include <vector>

using namespace std;

map<string, string> parseDict(ifstream& dictFile);
map<string, string> searchPrefix(map<string, string> dict);
void printDict(map<string, string> dict, int maxWords);

void error(string msg) {
  printf("Error: %s\n", msg.c_str());
  exit(1);
}

int main(int args, char *argv[]) {
  string dictFileName = "dictionary.txt";
  string prefix;
  string searchWord;
  string replaceWord;
  string editorPath;
  int numResults = 0;

  for (int i = 1; i < args; i++) {
    string arg = argv[i];
    if (!arg.compare("-d")) {
      dictFileName = argv[++i];
    } else if (!arg.compare("-p")) {
      prefix = argv[++i];
    } else if (!arg.compare("-n")) {
      numResults = stoi(argv[++i]);
    } else if (!arg.compare("-s")) {
      searchWord = argv[++i];
    } else if (!arg.compare("-r")) {
      replaceWord = argv[++i];
    } else if (!arg.compare("-v")) {
      editorPath = argv[++i];
    } else {
      error("invalid argument provided");
    }
  }

  ifstream dictFile(dictFileName.c_str());
  if (!dictFile) error("invalid filename provided");

  map<string, string> dict = parseDict(dictFile);
  printf("dictionary.txt has %d words.\n", (int) dict.size());

  if (!prefix.empty()) {
    map<string, string> prefixDict = searchPrefix(dict);
    int maxWords = numResults || prefixDict.size();
    printDict(prefixDict, maxWords);
  }

  return 0;
}

// a Trie DS could be used here instead of a map for faster prefix search times
map<string, string> parseDict(ifstream &dictFile) {
  map<string, string> dict;
  string word;
  while (getline(dictFile, word, ':')) {
    string definition;
    getline(dictFile, definition, '\n');
    if (!word.empty() && !definition.empty()) {
      dict[word] = definition;
    }
  }
  return dict;
}

map<string, string> searchPrefix(map<string, string> dict) {
  map<string, string> prefixDict;

  return prefixDict;
}

void printDict(map<string, string> dict, int maxWords) {
  
}
