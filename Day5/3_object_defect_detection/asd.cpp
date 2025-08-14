#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

typedef long long LL;

LL seg[400100], seg2[400001], A[400100];
LL N, M;

void init(LL s, LL e, LL node) {
    if(s==e) {
        seg[node] = A[s];
        seg2[node] = 0;
        return;
    }
    LL m = (s+e)/2;
    init(s, m, node*2);
    init(m+1, e, node*2+1);
    LL tmp[4] = {seg[node*2], seg[node*2+1], seg2[node*2], seg2[node*2+1]};
    sort(tmp, tmp+4);
    seg[node] = tmp[3];
    seg2[node] = tmp[2];
}

pair<LL, LL> getseg(LL s, LL e, LL node, LL qs, LL qe) {
    if(qe<s) return {0, 0};
    if(qs>e) return {0, 0};
    if(qs<=s && e<=qe) return {seg[node], seg2[node]};
    LL m = (s+e)/2;
    pair<LL, LL> n1 = getseg(s, m, node*2, qs, qe);
    pair<LL, LL> n2 = getseg(m+1, e, node*2+1, qs, qe);
    LL tmp[4] = {n1.first, n1.second, n2.first, n2.second};
    sort(tmp, tmp+4);
    //printf("getseg %lld %lld  %lld %lld\n", s, e, tmp[3], tmp[2]);
    return {tmp[3], tmp[2]};
}

void update(LL s, LL e, LL node, LL q, LL val) {
    if(s==e) {
        seg[node] = val;
        return;
    }
    LL m = (s+e)/2;
    if(q<=m) update(s, m, node*2, q, val);
    else update(m+1, e, node*2+1, q, val);
    LL tmp[4] = {seg[node*2], seg[node*2+1], seg2[node*2], seg2[node*2+1]};
    sort(tmp, tmp+4);
    seg[node] = tmp[3];
    seg2[node] = tmp[2];
}

int main () {
    scanf("%lld", &N);
    for(int i=1;i<=N;i++) scanf("%lld", &A[i]);
    init(1, N, 1);
    scanf("%lld", &M);
    for(int i=0;i<M;i++) {
        LL a, b, c;
        scanf("%lld %lld %lld", &a, &b, &c);
        if(a==1) {
            update(1, N, 1, b, c);
        } else if(a==2) {
            pair<LL, LL> hi = getseg(1, N, 1, b, c);
            printf("%lld\n", hi.first+hi.second);
        }
    }
}