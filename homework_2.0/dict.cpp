#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include <vector>
#include <regex>

using namespace std;

void checkFileName(string &dictFileName);
vector<pair<string, string>> parseDict(string dictFileName);
vector<pair<string, string>> searchPrefix(vector<pair<string, string>> dict, string prefix);
vector<pair<string, string>> searchAndReplace(vector<pair<string, string>> dict, string searchWord, string replaceWord);
void printDict(vector<pair<string, string>> dict, int maxWords);
void writeDict(vector<pair<string, string>> dict, string dictFileName);

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

  checkFileName(dictFileName);
  vector<pair<string, string>> dict = parseDict(dictFileName);
  printf("dictionary.txt has %d words.\n", (int) dict.size());

  if (!prefix.empty()) {
    vector<pair<string, string>> prefixDict = searchPrefix(dict, prefix);
    int maxWords = numResults ? numResults : prefixDict.size();
    printDict(prefixDict, maxWords);
  }

  if (!searchWord.empty() && !replaceWord.empty()) {
    vector<pair<string, string>> editedDict = searchAndReplace(dict, searchWord, replaceWord);
    writeDict(editedDict, dictFileName);
  }

  return 0;
}

void checkFileName(string &dictFileName) {
  ifstream dictFile(dictFileName.c_str());
  if (!dictFile) dictFileName = "dictionary.txt";
  else dictFile.close();
}

// a Trie DS could be used here instead of a map for faster prefix search time complexity
vector<pair<string, string>> parseDict(string dictFileName) {
  ifstream dictFile(dictFileName.c_str());
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
  dictFile.close();
  return dict;
}

vector<pair<string, string>> searchPrefix(vector<pair<string, string>> dict, string prefix) {
  vector<pair<string, string>> prefixDict;
  for (auto entry : dict) {
    string prefixRegex = "(" + prefix + ")(.*)";
    if (regex_match(get<0>(entry), regex(prefixRegex))) {
      prefixDict.push_back(entry);
    }
  }
  return prefixDict;
}

vector<pair<string, string>> searchAndReplace(vector<pair<string, string>> dict, string searchWord, string replaceWord) {
  vector<pair<string,string>> editedDict;
  for (auto entry : dict) {
    string replacedWord = regex_replace(get<0>(entry), regex(searchWord), replaceWord);
    string replacedDef = regex_replace(get<1>(entry), regex(searchWord), replaceWord);
    editedDict.push_back(make_pair(replacedWord, replacedDef));
  }
  return editedDict;
}

void printDict(vector<pair<string, string>> dict, int maxWords) {
  for (int i = 0; i < maxWords; i++) {
    printf("%s: %s\n", get<0>(dict[i]).c_str(), get<1>(dict[i]).c_str());
  }
}

void writeDict(vector<pair<string, string>> dict, string dictFileName) {
  ofstream dictFile(dictFileName.c_str());
  for (auto entry : dict) {
    dictFile << get<0>(entry) << ": " << get<1>(entry) << endl;
  }
  dictFile.close();
}

// g++ dict.cpp -g -O1 -o dict
