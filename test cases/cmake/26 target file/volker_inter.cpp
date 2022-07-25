#include <fstream>
#include <iostream>
int main(int argc, char *argv[]) {
  std::ofstream myfile;
  myfile.open(argv[1]);
  myfile << "int main(){}\n";
  myfile.close();
}
