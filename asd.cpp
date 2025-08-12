#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;
typedef long long LL;

LL arr[400001], seg[400001];
long long N, Q;
LL ans[100001];

vector<vector<LL>> query;

LL init(long long s, long long e, long long node) {
	//printf("init %lld %lld\n", s, e);
	if(s==e) {
		return seg[node]= arr[s];
	}
	int m = (s+e)/2;
	return seg[node]= init(s, m, node*2)+init(m+1, e, node*2+1);
}

LL getsum(LL s, LL e, LL node, LL qs, LL qe) {
	if(e<qs) return 0;
	if(s>qe) return 0;
	if(qs<=s && e<=qe) return seg[node];
	LL mid = (s+e)/2;
	return getsum(s, mid, node*2, qs, qe)+getsum(mid+1, e, node*2+1, qs, qe);
}

void update(LL s, LL e, LL node, LL q, LL v) {
	LL mid = (s+e)/2;
	if(s==e) {
		seg[node] = v;
		return;
	}
	if(q<=mid) update(s, mid, node*2, q, v);
	if(q>mid) update(mid+1, e, node*2+1, q, v);
	seg[node]=seg[node*2]+seg[node*2+1];
}

int main () {
	scanf("%lld", &N);
	for(long long i=1;i<=N;i++) {
		scanf("%lld", &arr[i]);
	}
	init(1, N, 1);
	scanf("%lld", &Q);
	LL NC=1, MC=0;
	for(long long i=1;i<=Q;i++) {
		long long a, b, c, d;
		scanf("%lld", &a);
		if(a==1) {
			scanf("%lld %lld", &b, &c);
			query.push_back({NC++, a, b, c});
		} else {
			scanf("%lld %lld %lld", &b, &c, &d);
			query.push_back({b, a, c, d, MC++});
		}
	}
	sort(query.begin(), query.end());
	for(int i=0;i<query.size();i++) {
		//printf("-%lld\n", query[i][1]);
		if(query[i][1] == 1) {
			update(1, N, 1, query[i][2], query[i][3]);
		} else {
			ans[query[i][4]] = getsum(1, N, 1, query[i][2], query[i][3]);
		}
	}
	for(int i=0;i<MC;i++) {
		printf("%lld\n", ans[i]);
	}
}

