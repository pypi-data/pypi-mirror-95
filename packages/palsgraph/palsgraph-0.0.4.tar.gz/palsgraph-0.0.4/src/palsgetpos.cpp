/**
 * Yujin Yao (pybind11 interface added by Yen Kaow Ng)
 */
#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstdlib>
#include <set>
#include <vector>
#include <map>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

using namespace std;

namespace py = pybind11;

const double FricCoe = 0.7;
const double NODE_MASS = 1;
const double GRAPH_SRING = 0.015;
const double CG_STRING = 0.5;
const double COMM_MASS = 2;
const double NODE_REPULSE = 0.015;
const double COMM_REPULSE = 1;


class Vec2 {
public:
    Vec2 () {
        a = 0;
        b = 0;
    }
    Vec2 (double a, double b) {
        this->a = a;
        this->b = b;
    }

    Vec2 operator+(const Vec2& other) const {
        return Vec2(a + other.a, b + other.b);
    }

    Vec2 operator-(const Vec2& other) const {
        return Vec2(a - other.a, b - other.b);
    }

    void operator+=(const Vec2& other) {
        a += other.a;
        b += other.b;
    }

    void operator*=(const double c) {
        a *= c;
        b *= c;
    }

    Vec2 unit() {
        return (*this) * (1.0l/len());
    }

    double len() {
        return sqrt(a * a + b * b);
    }

    Vec2 operator*(double c) {
        return Vec2(a * c, b * c);
    }

    string toString() {
        ostringstream s;
        s << a << ' ' << b;
        return s.str();
    }

    double get_x() { return a; }
    double get_y() { return b; }

    void bound(double l, double u) {
        a = max(min(a, u), l);
        b = max(min(b, u), l);
    }
private:
    double a, b;
};

class Node {
public:
    Node (int id, double mass) {
        this->id = id;
        pos = Vec2((double)rand()/(double)RAND_MAX, (double)rand()/(double)RAND_MAX);
        m = mass;
    }

    void clearForce() {
        accel = Vec2(0, 0);
    }

    void addForce(Vec2 f) {
        accel += f * (1.0l / m);
    }

    void move() {
        veloc += accel;
        veloc *= FricCoe;

        veloc.bound(-0.8, 0.8);

        pos += veloc;
    }

    int get_id() { return id; }
    double get_x() { return pos.get_x(); }
    double get_y() { return pos.get_y(); }

    void printSelf() {
        cout<<id<<' '<<pos.toString()<<endl;
    }
    Vec2 pos;
private:
    Vec2 veloc;
    Vec2 accel;
    double m;
    int id;
};

class String {
public:
    String(Node* a, Node* b, double coe) {
        this->a = a;
        this->b = b;
        this->coe = coe;
    }

    void tighten() {
        Vec2 dir = (a->pos - b->pos).unit();
        double dist = (a->pos - b->pos).len();
        if (abs(dist) < 0.01) return;
        double force = dist * coe;
        b->addForce(dir * force);
        a->addForce(dir * (-force));
    }
private:
    Node* a, *b;
    double coe;
};

void repulse(Node* a, Node* b, double coe) {
    Vec2 dis = b->pos - a->pos;
    double l = dis.len();
    if (l < 0.01) {
        l = 0.01;
    }
    Vec2 dir = dis.unit();
    a->addForce(dir * (-coe / l));
    b->addForce(dir * (coe / l));
}

const Vec2 center = Vec2(0.5, 0.5);
void gravityAttract(Node* n) {
    Vec2 dir = (center - n->pos).unit();
    double dist = (center - n->pos).len();
    if (abs(dist) < 0.01) return;
    double force = dist * GRAPH_SRING * 20;
    n->addForce(dir * force);
}


py::array_t<double> getpos(py::array_t<int> edges, py::array_t<int> clusters)
{
    srand(time(NULL));
    string s;
    map<int, Node*> nodes;
    vector<String*> strings;
    map<int, Node*> comms;

    auto buf1 = edges.request(), buf2 = clusters.request();

    int *ptr1 = (int *) buf1.ptr;
    int *ptr2 = (int *) buf2.ptr;

    int n_edges = buf1.shape[0];
    for (int i = 0; i < n_edges; i++)
    {
        int src = ptr1[i*2];
        int trg = ptr1[i*2 + 1];
        if (!nodes.count(src))
            nodes[src] = new Node(src, NODE_MASS);
        if (!nodes.count(trg))
            nodes[trg] = new Node(trg, NODE_MASS);
        strings.push_back(new String(nodes[src], nodes[trg], GRAPH_SRING));
    }

    int n_nodes = buf2.shape[0];
    for (int i = 0; i < n_nodes; i++)
    {
        int node = ptr2[i*2];
        int comm = ptr2[i*2 + 1];
        if (!comms.count(comm))
            comms[comm] = new Node(comm, COMM_MASS);
        strings.push_back(new String(nodes[node], comms[comm], CG_STRING));
    }

    vector<Node*> commsV, nodesV;
    for (auto c:comms) {
        commsV.push_back(c.second);
    }
    for (auto n:nodes) {
        nodesV.push_back(n.second);
    }
    int iter = 50;
    while (iter--) {
        for (auto c:commsV) {
            c->move();
            c->clearForce();
        }
        for (auto n:nodesV) {
            n->move();
            n->clearForce();
        }
        unsigned int i, j;
        for (i = 0; i < commsV.size(); i++) {
            for (j = i + 1; j < commsV.size(); j++) {
                repulse(commsV[i], commsV[j], COMM_REPULSE);
            }
        }
        for (i = 0; i < nodesV.size(); i++) {
            for (j = i + 1; j < nodesV.size(); j++) {
                repulse(nodesV[i], nodesV[j], NODE_REPULSE);
            }
        }
        for (auto n:nodesV) {
            gravityAttract(n);
        }
        for (auto c:commsV) {
            gravityAttract(c);
        }
        for (auto s:strings) {
            s->tighten();
        }
    }

    py::array_t<double> result = py::array_t<double>(n_nodes*3);
    auto buf3 = result.request();
    double *ptr3 = (double *) buf3.ptr;
    int count = 0;
    for (auto n:nodes) {
        if (n.second)
        {
            ptr3[count*3]   = (double)n.second->get_id();
            ptr3[count*3+1] = n.second->get_x();
            ptr3[count*3+2] = n.second->get_y();
        }
        //n.second->printSelf();
        count++;
    }

    result.resize({n_nodes, 3});
    return result;
}



PYBIND11_MODULE(palsgetpos, m){
    m.doc() = "palsgetpos by Yujin Yao";
    m.def("getpos", &getpos, "Compute node positions using palslayout");
}
