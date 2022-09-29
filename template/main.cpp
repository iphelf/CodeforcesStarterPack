#include <bits/stdc++.h>

using namespace std;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(nullptr);

  int n;
  int t;
  cin >> t;
  while (t--) {
    cin >> n;
    for (int i = 0; i < n; ++i)
      cout << i << (i == n - 1 ? '\n' : ' ');
  }
  return 0;
}
