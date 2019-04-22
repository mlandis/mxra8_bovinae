# python
import random
import subprocess
import numpy as np


def write_ctl(tmpl_fn, idx=1):

    s = ''
    s += 'seqfile = Mxra8.resample_' + str(idx) + '.fas\n'
    s += 'outfile = output/Mxra8.resample_' + str(idx) + '.out.txt\n'
    s += 'treefile = /Users/mlandis/projects/alphavirus_dating/data/emp/mxra8/mesquite/Mxra8.bovinae.no_insert.tre\n'

    ifn = open(tmpl_fn, 'r')
    for line in ifn:
        s += line
    ifn.close()

    ofn = open('codeml.ctl', 'w')
    ofn.write(s)
    ofn.close()
    return

ignore = '''
def sample_mtx(n_sample, taxa, align_fn):

    n_site = 0

    n_taxa = len(taxa)
    s = ''
    is_seq = False
    m = []
    tl = []
    for i in range(n_taxa):
        m.append([])

    inf = open(align_fn, 'r')
    taxon_lbl = ''
    taxon_idx = -1
    for line in inf:
        line = line.strip()
        if line[0] == '>' and line[1:] in taxa:
            is_seq = True
            taxon_lbl = line[1:]
            taxon_idx += 1
            print(taxon_idx)
            tl.append(taxon_lbl)
            #print(taxon_lbl)

        elif is_seq:
            is_seq = False
            if n_site == 0:
                n_site = int(len(line)/3)
                site_idx = random.choices( list(range(n_site)), k=n_sample)
            print(site_idx)
            for j,i in enumerate(site_idx):
                s = ''
                s += str(line[3*i+0]) + str(line[3*i+1]) + str(line[3*i+2])
                print('i='+str(i), 'j='+str(j), 'taxon_idx='+str(taxon_idx))
                print(3*i,s)
                m[taxon_idx].append(s)

    inf.close()
    return(tl, m)
'''

def sample_mtx(taxa, align_fn, n_sample=0, mask_invariant=True):

    n_site = 0
    n_taxa = len(taxa)
    s = ''
    is_seq = False
    m = []
    tl = []
    for i in range(n_taxa):
        m.append([])

    inf = open(align_fn, 'r')
    taxon_lbl = ''
    taxon_idx = -1
    for line in inf:
        line = line.strip()
        if line[0] == '>' and line[1:] in taxa:
            is_seq = True
            taxon_lbl = line[1:]
            taxon_idx += 1
            #print(taxon_idx)
            tl.append(taxon_lbl)
            #print(taxon_lbl)

        elif is_seq:
            is_seq = False
            if n_site == 0:
                n_site = int(len(line)/3)
                site_idx = range(0,n_site) #random.choices( list(range(n_site)), k=n_sample)
            for j,i in enumerate(site_idx):
                s = ''
                s += str(line[3*i+0]) + str(line[3*i+1]) + str(line[3*i+2])
                #print('i='+str(i), 'j='+str(j), 'taxon_idx='+str(taxon_idx))
                #print(3*i,s)
                m[taxon_idx].append(s)

    inf.close()

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

   
    if n_sample != 0:
        var_idx = random.choices( var_idx, k=n_sample ) 

    r_var = r[:, var_idx]

    return(tl, r_var)

def make_mtx_str(tl, m):
    s = ''
    for i in range(len(m)):
        s += '>' + tl[i] + '\n'
        for j in range(len(m[i])):
            s += m[i][j]
        s += '\n\n'
    return(s)


def check_mtx(m):
    print('CHECK_MTX')

    tf = []
    # for each codon site pos
    for j in range(len(m[0])):
        col_tf = True
        # for each taxon
        for i in range(2,len(m)):
            if 'N' in m[i][j] or '-' in m[i][j]:
                continue
            pair_tf = m[i-1][j] != m[i][j]
            col_tf = col_tf and pair_tf
        tf.append(tf)

    print(tf)
    return(False)


def sim_one(idx=1):
    fp = '/Users/mlandis/projects/alphavirus_dating/'
    code_fp = fp + 'code/mxra8/paml_basic_190421/'
    data_fp = fp + 'data/emp/mxra8/'

    align_fn = data_fp + 'Mxra8.no_insert.fas'
    out_fn = code_fp + 'sim/Mxra8.resample_' + str(idx) + '.fas'
    tree_fn = data_fp + 'mesquite/Mxra8.bovinae.no_insert.tre'
    ctl_fn = code_fp + 'sim/codeml.ctl'
    tmpl_fn = code_fp + 'sim/codeml_template.ctl'
    rslt_fn = code_fp + 'sim/output/Mxra8.resample_' + str(idx) + '.out.txt'

    taxa = ['Bos_indicus', 'Bos_taurus', 'Bos_primigenius', 'Bos_mutus', 'Bos_grunniens', 'Bos_javanicus', 'Bison_bison', 'Syncerus_caffer', 'Bubalus_bubalis', 'Tragelaphus_imberbis', 'Tragelaphus_angasii', 'Tragelaphus_eurycerus' ]

    n_units = 1
    unit_size = 5
    n_sample = unit_size * n_units

    tl,m = sample_mtx(taxa, align_fn, n_sample)

    #print(m)
    
    #return
    #tl,m = sample_mtx(n_sample, taxa, align_fn)

    #while check_mtx(m) is False:
    #    tl,m = sample_mtx(n_sample,taxa,align_fn)

    s_mtx = make_mtx_str(tl, m)
    print(s_mtx)
    #return(m)


    # write data
    #s += '>' + taxon_lbl + '\n'
    #for i in site_idx:
    #    s += str(line[3*i+0])
    #    s += str(line[3*i+1])
    #    s += str(line[3*i+2])
    #s += '\n\n'

    #inf.close()

    outf = open(out_fn, 'w')
    outf.write(s_mtx)
    outf.close()

    # write codeml file
    write_ctl(tmpl_fn, idx)

    # now run PAML
    rslt = subprocess.call(['codeml'])
    rsltf = open(rslt_fn, 'r')
    for line in rsltf:
        line = line.strip()
        if 'omega' in line:
            omega = line.split(' ')[-1]
            print('omega = ' + omega)

    return(omega)


vals = []
for i in range(300):
    vals.append( sim_one(i) )


print(vals)
outf = open('vals.3.txt', 'w')
[ outf.write(x+'\n') for x in vals ]
outf.close()
