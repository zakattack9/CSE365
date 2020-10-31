#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

using namespace std;

vector<pair<string, string>> parseDict(ifstream& dictFile);
vector<pair<string, string>> searchPrefix(vector<pair<string, string>> dict, string prefix);
void printDict(vector<pair<string, string>> dict, int maxWords);

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

  vector<pair<string, string>> dict = parseDict(dictFile);
  printf("dictionary.txt has %d words.\n", (int) dict.size());

  if (!prefix.empty()) {
    vector<pair<string, string>> prefixDict = searchPrefix(dict, prefix);
    int maxWords = numResults ? numResults : prefixDict.size();
    printDict(prefixDict, maxWords);
  }

  return 0;
}

// a Trie DS could be used here instead of a map for faster prefix search times
vector<pair<string, string>> parseDict(ifstream &dictFile) {
  vector<pair<string, string>> dict;
  string word;
  while (getline(dictFile, word, ':')) {
    string definition;
    getline(dictFile, definition, '\n');
    if (!word.empty() && !definition.empty()) {
      if (definition[0] == ' ') definition.erase(0, 1); // remove space after :
      dict.push_back(make_pair(word, definition));
    }
  }
  return dict;
}

vector<pair<string, string>> searchPrefix(vector<pair<string, string>> dict, string prefix) {
  vector<pair<string, string>> prefixDict;
  for (auto entry : dict) {
    bool isPrefix = true;
    for (int i = 0; i < prefix.length(); i++) {
      if (get<0>(entry)[i] != prefix[i]) {
        isPrefix = false;
        break;
      }
    }
    if (isPrefix) prefixDict.push_back(entry);
  }
  return prefixDict;
}

void printDict(vector<pair<string, string>> dict, int maxWords) {
  for (int i = 0; i < maxWords; i++) {
    printf("%s: %s\n", get<0>(dict[i]).c_str(), get<1>(dict[i]).c_str());
  }
}

// g++ dict.cpp -g -O1 -o dict
