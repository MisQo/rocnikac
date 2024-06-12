#include <bits/stdc++.h>
#include "table.cpp"
using namespace std;

vector<double> seq_signal(string s){
    map<char, int> alp = {{'A', 0}, {'C', 1}, {'G', 2}, {'T', 3}};

    vector<double> res;
    int cur = 0;
    for(int i = 0; i < s.size(); i++)
    {
        cur *= 4;
        cur += alp[s[i]];
        if(i > 4)
        {
            res.push_back(table[cur]);
            cur %= 1024;
        }
    }
    return res;
}

struct DPstate{
    double avg_err;
    double sum_err;
    int index;
    int previous_index;

    DPstate(double a, double s, int i, int p){
        avg_err = a;
        sum_err = s;
        index = i;
        previous_index = p;
    }
};

bool operator<(const DPstate &a, const DPstate &b)
{
    return a.avg_err < b.avg_err;
}

vector<int> generate_move(vector<double> signal, string sequence, int l, int r, int width) {
    auto seq = seq_signal(sequence);
    int n = signal.size(), k = seq.size();
    vector<vector<DPstate>> memo(2, vector<DPstate>(signal.size()+1, DPstate(INFINITY, INFINITY, -1, -1)));
    memo[0][0] = DPstate(0, 0, 0, -1);
    map<pair<int, int>, int> old;


    for(int t = 0; t < k; t++)
    {
        int id = t&1;
        sort(memo[id].begin(), memo[id].end());
        memo[!id].assign(signal.size(), DPstate(INFINITY, INFINITY, -1, -1));
        int poc = width-1;
        for(auto state : memo[id])
        {
            poc--;
            if(!poc) break;
            if(state.index == -1) break;
            // cout << state.avg_err << ' ' << state.sum_err << ' ' << state.index << ' ' << state.previous_index << endl;
            int i = state.index;
            old[{t, i}] = state.previous_index;
            double cur_err = state.sum_err;
            for(int x = 0; x < l; x++)
            {
                if(i + x > n) break;
                cur_err += (signal[i+x] - seq[t])*(signal[i+x]-seq[t]);
            }
            for(int x = l; x < r; x++)
            {
                if(i+x > n) break;
                if(i+x + (k-t-1) * l <= n && i + x + (k-t-1) * (r-1) >= n)
                {
                    memo[!id][i+x] = min(memo[!id][i+x], DPstate(cur_err/(i+x), cur_err, i+x, i));
                    // cout << "penis\n" << i << ' ' << x << ' ' << n << endl;
                    // cout << cur_err << ' ' << memo[!id][i+x].avg_err << endl;

                }
                if(i+x >= n) break;
                cur_err += (signal[i+x] - seq[t])*(signal[i+x]-seq[t]);
                // // for(auto x : memo[!id]) cout << x.avg_err << ' ' << x.sum_err << ' ' << x.index << ' ' << x.previous_index << endl;
            }
        }
    }
    old[{k, n}] = memo[k&1][n].previous_index;

    // cout << "old\n";
    // for (auto const& [key, val] : old) cout << key.first << ' ' << key.second << ' ' << val << endl;
    
    // cout << '\n';
    // cout << 'k' << k << " n" << n << endl;

    vector<int> move(n, 0);
    int c = n;
    for(int i = k; i > 1; i--)
    {
        // cout << c << i << endl;
        move[old[{i, c}]] = 1;
        c = old[{i, c}];
    }

    return move;



    vector<int> res(signal.size(), 0);
    for(int i = 1; i <= sequence.size()-6; i++)
        res[i] = 1;
    return res;
}

