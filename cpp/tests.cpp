#include "core.hpp"
#include <cassert>
#include <cmath>
int main(){sumi::WindowEngine e(60,2);assert(e.ingest(-1,"soil",2));assert(e.ingest(0,"soil",4));assert(e.ingest(59,"soil",6));assert(e.windows().size()==2);assert(e.windows().begin()->first.first==-60);assert(!e.ingest(60,"soil",8));assert(!e.ingest(0,"",1));assert(!e.ingest(0,"soil",NAN));assert(e.windows().at({0,"soil"}).mean()==5);e.clear();assert(e.windows().empty());}
