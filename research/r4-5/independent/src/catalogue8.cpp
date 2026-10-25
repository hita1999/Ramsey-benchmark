// Exhaust all 2^(n choose 2) labeled graphs, n <= 8. No nauty/canonicalizer.
// Compare the exact Ramsey predicate with the union of every permutation of
// every input graph. This checks soundness AND completeness of the catalogue.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using U=uint32_t;
int main(int argc,char**argv) {
  if(argc!=5) throw std::runtime_error("usage: catalogue8 file.g6 n s t");
  int n=std::stoi(argv[2]),s=std::stoi(argv[3]),t=std::stoi(argv[4]);
  if(n<1||n>8||s<2||t<2||s>n||t>n) throw std::runtime_error("unsupported dimensions");
  int index[8][8]={},m=0;
  for(int j=1;j<n;++j)for(int i=0;i<j;++i)index[i][j]=index[j][i]=m++;
  std::vector<U> clique_masks,independent_masks;
  for(U v=0;v<(1u<<n);++v) {
    int k=__builtin_popcount(v); if(k!=s&&k!=t)continue;
    U mask=0;
    for(int j=1;j<n;++j)for(int i=0;i<j;++i)
      if((v>>i&1u)&&(v>>j&1u))mask|=1u<<index[i][j];
    if(k==s)clique_masks.push_back(mask);
    if(k==t)independent_masks.push_back(mask);
  }
  auto valid=[&](U graph) {
    for(U q:clique_masks)if((graph&q)==q)return false;
    for(U q:independent_masks)if((graph&q)==0)return false;
    return true;
  };
  const U total=1u<<m;
  std::vector<uint64_t> covered((total+63ull)/64);
  std::set<U> canonical;
  std::ifstream in(argv[1]); if(!in)throw std::runtime_error("cannot open catalogue");
  std::string line; int graphs=0; uint64_t permutations=0,orbit_union=0;
  while(std::getline(in,line)) {
    if(!line.empty()&&line.back()=='\r')line.pop_back();
    if(line.size()!=1+(m+5)/6 || static_cast<unsigned char>(line[0])-63!=n)
      throw std::runtime_error("bad graph6 length/order");
    for(char c:line)if(c<63||c>126)throw std::runtime_error("bad graph6 character");
    U graph=0;
    for(int k=0;k<m;++k)if(((line[1+k/6]-63)>>(5-k%6))&1)graph|=1u<<k;
    for(int k=m;k<6*((m+5)/6);++k)
      if(((line[1+k/6]-63)>>(5-k%6))&1)throw std::runtime_error("nonzero padding");
    if(!valid(graph))throw std::runtime_error("invalid representative");
    std::vector<int> p(n); std::iota(p.begin(),p.end(),0); U minimum=total;
    do {
      U permuted=0;
      for(int j=1;j<n;++j)for(int i=0;i<j;++i)
        if(graph>>index[i][j]&1u)permuted|=1u<<index[p[i]][p[j]];
      minimum=std::min(minimum,permuted);
      auto &word=covered[permuted/64]; uint64_t bit=1ull<<(permuted%64);
      if(!(word&bit)){word|=bit;++orbit_union;} ++permutations;
    }while(std::next_permutation(p.begin(),p.end()));
    if(!canonical.insert(minimum).second)throw std::runtime_error("isomorphic duplicates");
    ++graphs;
  }
  uint64_t accepted=0;
  for(U graph=0;graph<total;++graph) {
    bool good=valid(graph), listed=(covered[graph/64]>>(graph%64))&1ull;
    if(good!=listed) {
      std::cerr<<"classification mismatch at labeled mask "<<graph<<"\n";return 1;
    }
    accepted+=good;
  }
  std::cout<<"{\"n\":"<<n<<",\"s\":"<<s<<",\"t\":"<<t
    <<",\"representatives\":"<<graphs<<",\"labeled_graphs_checked\":"<<total
    <<",\"valid_labeled_graphs\":"<<accepted<<",\"orbit_union\":"<<orbit_union
    <<",\"permutations_checked\":"<<permutations<<",\"status\":\"COMPLETE\"}\n";
}
