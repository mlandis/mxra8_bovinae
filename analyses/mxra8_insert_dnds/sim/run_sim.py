# python
import random
import subprocess
import numpy as np

# write a new control file for the replicate idx
def write_ctl(tmpl_fn, idx=1):
    # make header str
    s = ''
    s += 'seqfile = ../data/sim/Mxra8.resample_' + str(idx) + '.fas\n'
    s += 'outfile = output/Mxra8.resample_' + str(idx) + '.out.txt\n'
    s += 'treefile = ../data/Mxra8.bovinae.no_insert.tre\n'
    # append template footer st
    ifn = open(tmpl_fn, 'r')
    for line in ifn:
        s += line
    ifn.close()
    # write new file
    ofn = open('codeml.ctl', 'w')
    ofn.write(s)
    ofn.close()
    # done
    return

# generate codon bootstrap matrix
def sample_mtx(taxa, align_fn, n_sample=0, mask_invariant=True):
    # init variables
    n_site = 0
    n_taxa = len(taxa)
    s = ''
    is_seq = False
    taxon_lbl = ''
    taxon_idx = -1
    m = []
    tl = []
    for i in range(n_taxa):
        m.append([])
    # read file
    inf = open(align_fn, 'r')
    for line in inf:
        line = line.strip()
        # line is taxon label
        if line[0] == '>' and line[1:] in taxa:
            is_seq = True
            taxon_lbl = line[1:]
            taxon_idx += 1
            tl.append(taxon_lbl)
        # line is sequence data
        elif is_seq:
            is_seq = False
            # get all sites
            if n_site == 0:
                n_site = int(len(line)/3)
                site_idx = range(0,n_site)
            # store codon str into matrix m
            for j,i in enumerate(site_idx):
                s = ''
                s += str(line[3*i+0]) + str(line[3*i+1]) + str(line[3*i+2])
                m[taxon_idx].append(s)
    # close file
    inf.close()
    # filter invariant codon sites out of matrix
    var_idx = []
    r = np.array(m)
    for i in range(r.shape[1]):
        if mask_invariant is False:
            var_idx.append(i)
        else:
            col = r[:,i]
            col = [ x for x in col if '-' not in x and 'N' not in x and 'TAG' not in x ]
            col_unique = np.unique(col)
            if len(col_unique) > 1:
                var_idx.append(i)
    # sample codon sites 
    if n_sample != 0:
        var_idx = random.choices( var_idx, k=n_sample ) 
    # extract codon sites from total mtx
    r_var = r[:, var_idx]
    # done!
    return(tl, r_var)

# converts matrix into a fasta file string
def make_mtx_str(tl, m):
    s = ''
    for i in range(len(m)):
        s += '>' + tl[i] + '\n'
        for j in range(len(m[i])):
            s += m[i][j]
        s += '\n\n'
    return(s)


# generate one bootstrap replicate
def sim_one(idx=1):
    fp = '/Users/mlandis/projects/mxra8_bovinae/analyses/mxra8_insert_dnds/'
    code_fp = fp + './'
    data_fp = fp + 'data/'

    align_fn = data_fp + 'Mxra8.no_insert.fas'
    tree_fn  = data_fp + 'Mxra8.bovinae.no_insert.tre'
    out_fn   = data_fp + 'sim/Mxra8.resample_' + str(idx) + '.fas'
    ctl_fn   = code_fp + 'sim/codeml.ctl'
    tmpl_fn  = code_fp + 'sim/codeml_template.ctl'
    rslt_fn  = code_fp + 'sim/output/Mxra8.resample_' + str(idx) + '.out.txt'
    
    # get taxa we want
    taxa = ['Bos_indicus', 'Bos_taurus', 'Bos_primigenius', 'Bos_mutus', 'Bos_grunniens', 'Bos_javanicus', 'Bison_bison', 'Syncerus_caffer', 'Bubalus_bubalis', 'Tragelaphus_imberbis', 'Tragelaphus_angasii', 'Tragelaphus_eurycerus' ]

    # bootstrap dimensions
    n_units = 1
    unit_size = 5
    n_sample = unit_size * n_units

    # sample mtx
    tl,m = sample_mtx(taxa, align_fn, n_sample)

    # make fasta str
    s_mtx = make_mtx_str(tl, m)

    # write fasta str
    outf = open(out_fn, 'w')
    outf.write(s_mtx)
    outf.close()

    # write codeml file
    write_ctl(tmpl_fn, idx)

    # now run PAML
    rslt = subprocess.call(['codeml'])
    rsltf = open(rslt_fn, 'r')
    omega = 0
    for line in rsltf:
        line = line.strip()
        if 'omega' in line:
            omega = line.split(' ')[-1]
            print('omega = ' + omega)
    return(omega)


vals = []
for i in range(2):
    vals.append( sim_one(i) )


print(vals)
outf = open('vals.3.txt', 'w')
[ outf.write(x+'\n') for x in vals ]
outf.close()


