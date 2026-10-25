// Independent of verify_lower24.py: construct undirected edges by adding offsets,
// then enumerate fixed-popcount integer masks and count induced edges.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>

int main() {
  std::array<uint32_t,24> adj{};
  for (int i=0;i<24;++i) for (int step : {1,2,4,8,9}) {
    int j=(i+step)%24;
    adj[i]|=1u<<j; adj[j]|=1u<<i;
  }
  int degree_sum=0;
  for (int i=0;i<24;++i) {
    if ((adj[i]>>i)&1u || __builtin_popcount(adj[i])!=10)
      throw std::runtime_error("invalid adjacency/degree");
    degree_sum+=__builtin_popcount(adj[i]);
  }
  uint64_t checked[2]={}, forbidden[2]={};
  for (int k : {4,5}) {
    uint32_t mask=(1u<<k)-1;
    while (mask<(1u<<24)) {
      int twice_edges=0;
      for (int v=0;v<24;++v) if ((mask>>v)&1u)
        twice_edges+=__builtin_popcount(adj[v]&mask);
      ++checked[k-4];
      if ((k==4 && twice_edges==12) || (k==5 && twice_edges==0))
        ++forbidden[k-4];
      uint32_t low=mask&-mask, carry=mask+low;
      mask=carry|(((carry^mask)>>2)/low);
    }
  }
  if (checked[0]!=10626 || checked[1]!=42504 || forbidden[0] || forbidden[1])
    throw std::runtime_error("exhaustive verification failed");
  std::cout << "{\"vertices\":24,\"edges\":" << degree_sum/2
    << ",\"degree\":10,\"four_subsets_checked\":" << checked[0]
    << ",\"five_subsets_checked\":" << checked[1]
    << ",\"k4_count\":" << forbidden[0]
    << ",\"independent5_count\":" << forbidden[1]
    << ",\"lower_bound\":25,\"status\":\"VERIFIED\"}\n";
}
