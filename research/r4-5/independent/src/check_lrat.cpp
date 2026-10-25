// Independent positive-hint LRAT checker. No solver code or libraries.
// Accepts RUP additions only; negative RAT hints are rejected. Deletions are
// ignored (keeping already proved consequences is sound for RUP).
#include <algorithm>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <vector>
using Clause=std::vector<int>;
using ID=long long;
void require(bool b,const char*msg){if(!b)throw std::runtime_error(msg);}
int main(int argc,char**argv)try {
  require(argc==3,"usage: check_lrat formula.cnf proof.lrat");
  std::ifstream cnf(argv[1]),proof(argv[2]);
  require(bool(cnf)&&bool(proof),"cannot open input");
  std::string line,word; int nv=-1; ID expected=-1,next=0;
  std::unordered_map<ID,Clause> db;
  while(std::getline(cnf,line)) {
    std::istringstream row(line); if(!(row>>word)||word=="c")continue;
    if(word=="p") {
      require(nv<0,"duplicate header");
      require(bool(row>>word>>nv>>expected)&&word=="cnf"&&nv>=0&&expected>=0,"bad header");
      require(!(row>>word),"trailing header text"); continue;
    }
    require(nv>=0,"missing header");
    std::istringstream lits(line); Clause c; long long lit; bool ended=false;
    while(lits>>lit){
      if(!lit){ended=true;break;}
      require(lit>=-nv&&lit<=nv,"out of range literal"); c.push_back(int(lit));
    }
    require(ended&&!(lits>>word),"one terminated clause per line required");
    std::sort(c.begin(),c.end()); c.erase(std::unique(c.begin(),c.end()),c.end());
    db.emplace(++next,std::move(c));
  }
  require(nv>=0&&next==expected,"CNF clause count mismatch");
  ID additions=0,deletions=0,hints=0,last=next; bool empty=false;
  while(std::getline(proof,line)) {
    std::istringstream row(line); if(!(row>>word))continue;
    if(word=="c")continue;
    size_t pos=0; ID id=std::stoll(word,&pos);
    require(pos==word.size()&&id>0,"bad proof ID");
    require(bool(row>>word),"missing proof payload");
    if(word=="d") {
      ID x; bool ended=false;
      while(row>>x){if(x==0){ended=true;break;}require(x>0&&db.count(x),"bad deletion ID");}
      require(ended&&!(row>>word),"malformed deletion");++deletions;continue;
    }
    require(id>last&&!db.count(id),"non-increasing addition ID");
    Clause clause; bool terminated=false;
    do {
      size_t p=0; long long lit=std::stoll(word,&p);
      require(p==word.size()&&lit>=-nv&&lit<=nv,"bad proof literal");
      if(lit==0){terminated=true;break;} clause.push_back(int(lit));
    }while(row>>word);
    require(terminated,"unterminated proof clause");
    std::sort(clause.begin(),clause.end());
    clause.erase(std::unique(clause.begin(),clause.end()),clause.end());
    std::vector<int> values(nv+1,0); bool conflict=false;
    auto assign=[&](int lit) {
      int v=std::abs(lit),value=lit>0?1:-1;
      if(values[v]&&values[v]!=value){conflict=true;return;}
      values[v]=value;
    };
    for(int lit:clause)assign(-lit);
    ID hint; bool end_hints=false;
    while(row>>hint) {
      if(hint==0){end_hints=true;break;}
      require(hint>0&&db.count(hint),"unknown or unsupported RAT hint");++hints;
      if(conflict)continue;
      int unassigned=0,unit=0; bool satisfied=false;
      for(int lit:db.at(hint)) {
        int val=values[std::abs(lit)]*(lit>0?1:-1);
        if(val>0){satisfied=true;break;}
        if(val==0){++unassigned;unit=lit;}
      }
      require(!satisfied&&unassigned<=1,"hint is neither unit nor conflicting");
      if(unassigned==0)conflict=true;else assign(unit);
    }
    require(end_hints&&!(row>>word),"malformed hints");
    require(conflict,"RUP check did not derive conflict");
    empty=empty||clause.empty();db.emplace(id,std::move(clause));last=id;++additions;
  }
  require(empty,"proof has no verified empty clause");
  std::cout<<"{\"status\":\"VERIFIED_UNSAT\",\"additions\":"<<additions
    <<",\"deletion_lines_ignored\":"<<deletions<<",\"hints_checked\":"<<hints<<"}\n";
  return 0;
}catch(const std::exception&e){std::cerr<<"REJECTED: "<<e.what()<<"\n";return 1;}
