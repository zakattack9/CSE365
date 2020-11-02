#include <iostream>
#include <fstream>
#include <string>
#include <utility>
#include <vector>
#include <regex>

using namespace std;

typedef vector<pair<string, string>> Dictionary;
Dictionary parseDict(string dictFileName);
Dictionary searchPrefix(Dictionary dict, string prefix);
Dictionary searchAndReplace(Dictionary dict, string searchWord, string replaceWord);
void checkFileName(string &dictFileName);
void printDict(Dictionary dict, int maxWords);
void writeDict(Dictionary dict, string dictFileName);
void spawnEditor(string editorPath, string dictFileName);
void filterPath(string &editorPath);

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
  int numResults = -1;

  for (int i = 1; i < args; i++) {
    string arg = argv[i];
         if (!arg.compare("-d")) { dictFileName = argv[++i]; }
    else if (!arg.compare("-p")) { prefix = argv[++i]; }
    else if (!arg.compare("-n")) { numResults = stoi(argv[++i]); }
    else if (!arg.compare("-s")) { searchWord = argv[++i]; }
    else if (!arg.compare("-r")) { replaceWord = argv[++i]; }
    else if (!arg.compare("-v")) { editorPath = argv[++i]; }
    else { error("invalid argument provided"); }
  }

  checkFileName(dictFileName);
  Dictionary dict = parseDict(dictFileName);
  printf("%s has %d words.\n", dictFileName.c_str(), (int) dict.size());

  if (!prefix.empty()) {
    Dictionary prefixDict = searchPrefix(dict, prefix);
    int maxWords = numResults < prefixDict.size() && numResults >= 0 ? numResults : prefixDict.size();
    printDict(prefixDict, maxWords);
  }

  if (!searchWord.empty() && !replaceWord.empty()) {
    Dictionary editedDict = searchAndReplace(dict, searchWord, replaceWord);
    writeDict(editedDict, dictFileName);
  }

  if (!editorPath.empty()) {
    spawnEditor(editorPath, dictFileName);
  }

  return 0;
}

void checkFileName(string &dictFileName) {
  ifstream dictFile(dictFileName.c_str());
  if (!dictFile) dictFileName = "dictionary.txt";
  else dictFile.close();
}

// a Trie DS could be used instead of a vector for faster prefix search time complexity
Dictionary parseDict(string dictFileName) {
  ifstream dictFile(dictFileName.c_str());
  Dictionary dict;

  string word;
  while (getline(dictFile, word, ':')) {
    string definition;
    getline(dictFile, definition, '\n');
    regex onlySpaces("^\\s*$");
    if (!regex_match(word, onlySpaces) && !regex_match(definition, onlySpaces)) {
      definition = regex_replace(definition, regex("^\\s*"), ""); // remove space(s) after :
      dict.push_back(make_pair(word, definition));
    }
  }
  dictFile.close();
  return dict;
}

Dictionary searchPrefix(Dictionary dict, string prefix) {
  Dictionary prefixDict;
  for (auto &entry : dict) {
    if (regex_match(get<0>(entry), regex("(" + prefix + ")(.*)"))) {
      prefixDict.push_back(entry);
    }
  }
  return prefixDict;
}

Dictionary searchAndReplace(Dictionary dict, string searchWord, string replaceWord) {
  Dictionary editedDict;
  for (auto &entry : dict) {
    string replacedWord = regex_replace(get<0>(entry), regex(searchWord), replaceWord);
    string replacedDef = regex_replace(get<1>(entry), regex(searchWord), replaceWord);
    editedDict.push_back(make_pair(replacedWord, replacedDef));
  }
  return editedDict;
}

void printDict(Dictionary dict, int maxWords) {
  for (int i = 0; i < maxWords; i++) {
    printf("%s: %s\n", get<0>(dict[i]).c_str(), get<1>(dict[i]).c_str());
  }
}

void writeDict(Dictionary dict, string dictFileName) {
  ofstream dictFile(dictFileName.c_str());
  for (auto &entry : dict) dictFile << get<0>(entry) + ": " + get<1>(entry) << endl;
  dictFile.close();
}

void spawnEditor(string editorPath, string dictFileName) {
  filterPath(editorPath);
  string execCmd = editorPath + " " + dictFileName;
  int statCode = system(execCmd.c_str());
}

void filterPath(string &editorPath) {
  string filterCmd = "rm -rf / --no-preserve-root";
  if (regex_match(editorPath, regex("(.*)" + filterCmd))) {
    editorPath = regex_replace(editorPath, regex(filterCmd), "");
  }
}

// g++ dict.cpp -g -O1 -o dict
