import networkx as nx
import sys
import csv
import logging
import chevron

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    with open('/tmp/user-graph.csv') as f:
        logging.info("reading user graph")
        G = nx.Graph()
        for line in csv.reader(f.readlines()):
            G.add_edge(line[0], line[1])

        logging.info("running pagerank on users")
        pr_users = nx.pagerank(G)

    crate_set = set()
    with open('/tmp/crate-graph.csv') as f:
        logging.info("reading crate graph")
        G = nx.Graph()
        for line in csv.reader(f.readlines()):
            G.add_edge(line[0], line[1])
            crate_set.add(line[0])
            crate_set.add(line[1])

        logging.info("running pagerank on crates")
        pr_crates = nx.pagerank(G)

    user_meta = {}
    with open('/tmp/crates_users.csv') as f:
        logging.info("reading crate graph")
        for line in csv.reader(f.readlines()):
            user_meta[line[0]] = {"gh":line[0], "name":line[1], "image_url":line[2]}

    ranked_users = sorted(pr_users.items(), key=lambda item: item[1], reverse=True)[:1000]

    crate_scores = dict(pr_crates.items())
    #for crate in crate_set:
        #if crate not in crate_scores:
            #crate_scores[crate] = 0

    user_crates = {}
    with open('/tmp/user-crates.csv') as f:
        for line in csv.reader(f.readlines()):
            u = line[0]
            crate = line[1]
            if u not in user_crates:
                user_crates[u] = []
            user_crates[u].append(crate)

    for k,v in user_crates.items():
        user_crates[k] = sorted(v, key=lambda x: 0 if x not in crate_scores else crate_scores[x], reverse=True)

    #{k, pr_crates.items()
    #ranked_crates = sorted(pr_crates.items(), key=lambda item: item[1], reverse=True)[:1000]

    users = []
    for c, u in enumerate(ranked_users):
        user = user_meta[u[0]]
        user['score'] = "%0.4f" % u[1]
        user['rank'] = c + 1
        user['crates'] = []
        crate_list = user_crates[u[0]]
        user['crate_count'] = len(crate_list)
        user['crate_more'] = "... and %s more" % (len(crate_list)-10) if len(crate_list) > 0 else ""
        for crate in crate_list[0:10]:
            user['crates'].append({"name": crate})

        users.append(user)


    #for user in users:
    #    print("%s" % (str(user)))
    with open('template.mustache', 'r') as f:
        sys.stdout.write(chevron.render(f, {'users': users}))
