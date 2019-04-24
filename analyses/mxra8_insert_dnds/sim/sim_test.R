x15 = read.table('vals.n15.txt')[,1]
x30 = read.table('vals.n30.txt')[,1]

f15 = sum(x15 > 1)/length(x15)
f30 = sum(x30 > 1)/length(x30)

fp = '/Users/mlandis/projects/mxra8_bovinae/analyses/mxra8_insert_dnds/output/'
fn = c( "Mxra8.bovinae.insert.L5.out.txt",
        "Mxra8.bovinae.insert.D5.out.txt",
        "Mxra8.bovinae.insert.D10.out.txt",
        "Mxra8.bovinae.insert_flank.L5.out.txt",
        "Mxra8.bovinae.insert_flank.D5.out.txt",
        "Mxra8.bovinae.insert_flank.D10.out.txt",
        "Mxra8.bovinae.no_insert.out.txt" )

hn = c("L5","D5","D10","L5","D5","D10","null")
sn = c("insert","insert","insert","insert+flank","insert+flank","insert+flank","background")

omega = c()
for (i in 1:length(fn))
{
    ff = paste(fp, fn[i], sep="")
    l = readLines(ff)
    
    if (i == 7) {
        s = grep('omega',l)
        s = s[length(s)]
        stok = strsplit(x=l[s],split=" ")[[1]][5]
    }
    else {
        s = grep('for branches',l)
        s = s[length(s)]
        stok = strsplit(x=l[s],split=" ")[[1]][7]
    }
    omega = c(omega, stok)
}
omega = as.numeric(omega)

df = data.frame( history=hn, sites=sn, omega=omega, stringsAsFactors=F)
df$ns = c(15, 15, 30, 15, 15, 30, 0)
df$p_pos = rep(0, 7)
df$p_emp = rep(0, 7)


sapply( df$omega[df$ns==15], function(x) { sum(x15 > x)/length(x15) } )
df$p_emp[df$ns==15] = sapply( df$omega[df$ns==15], function(x) { sum(x15 > x)/length(x15) } )
df$p_pos[df$ns==15] = sapply( df$omega[df$ns==15], function(x) { sum(x15 > 1)/length(x15) } )
df$p_emp[df$ns==30] = sapply( df$omega[df$ns==30], function(x) { sum(x30 > x)/length(x30) } )
df$p_pos[df$ns==30] = sapply( df$omega[df$ns==30], function(x) { sum(x30 > 1)/length(x30) } )

df

#sum(dat[,1] > 1)/nrow(dat)
#sum(dat[,1] > 1.8)/nrow(dat)
