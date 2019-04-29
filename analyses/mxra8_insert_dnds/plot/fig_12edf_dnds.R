library(ggplot2)

x15 = read.table('vals.n15.txt')[,1]
x30 = read.table('vals.n30.txt')[,1]

r15 = range(sort(x15)[1:475])
r30 = range(sort(x30)[1:475])

f15 = sum(x15 >= 1)/length(x15)
f30 = sum(x30 >= 1)/length(x30)

fp = '/Users/mlandis/projects/mxra8_bovinae/analyses/mxra8_insert_dnds/output/'
fn = c( "Mxra8.bovinae.insert.L5.out.txt",
        "Mxra8.bovinae.insert.D5.out.txt",
        "Mxra8.bovinae.insert.D10.out.txt",
        "Mxra8.bovinae.insert_flank.L5.out.txt",
        "Mxra8.bovinae.insert_flank.D5.out.txt",
        "Mxra8.bovinae.insert_flank.D10.out.txt",
        "Mxra8.bovinae.no_insert.out.txt" )

hn = c("L5","D5","D10","L5","D5","D10","")
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



# 
# dn = c("L5", "D5", "D10", "L5", "D5", "D10", "background")
# sn = c("insert","insert","insert","insert+flank","insert+flank","insert+flank","no insert")
# 
# xx = c( 1.52356,
#         1.28926,
#         1.38234,
#         1.40917,
#         1.22705,
#         1.39503,
#         0.16929 )
# df = data.frame( data=dn, sites=sn, omega=xx )

df$data_site = paste( df$history, df$sites, sep="\n" )
df$data_site = as.vector(df$data_site)
df$data_site[7] = "background"
ds_lvl = df$data_site

df$data_site = factor(df$data_site, ordered=T, levels=rev(ds_lvl))
#df$history = factor(df$history, ordered=T, levels=rev(levels(df$history)))

p = ggplot(df, aes(x=omega, y=data_site))
p = p + xlab("dN/dS estimate")
p = p + ylab("Condition")
p = p + xlim(0,2.5)
p = p + geom_point(size=3)
p = p + geom_vline(xintercept = 1, linetype=2, colour="blue")
p = p + geom_vline(xintercept = max(r15), linetype=2, colour="red")
p = p + annotate( "text", x = 1.35, y = 7, label="positive selection\ndN/dS > 1.00", hjust=0.5, size=2.5, col="blue")
p = p + annotate( "text", x = 0.3, y = 7, label="95% of background\nbootstrap replicates\ndN/dS < 0.69", hjust=0.5, size=2.5, col="red")
#p = p + scale_colour_discrete( values=c("red","blue","black") )
#p = p + scale_x_reverse()
#p = p + scale_x_discrete(limits = rev(levels(df$data_site)))
dfx = data.frame(x=sort(x15)[1:475])

#p = ggplot(dfx, aes(x))
#p = p + stat_bin(data=dfx, mapping=aes(x=x), bins=50, geom="step")
#p = p + geom_density( data=dfx ) #, mapping=aes(x=x) )
p = p + theme_bw()
p = p + theme(panel.border = element_blank(),
              panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              axis.line = element_line(colour = "black"),
              axis.text.y = element_text(hjust=0.5))
#p = p +  scale_x_continuous(trans = "reverse", breaks = unique(df$data))
p = p + guides(size=FALSE)
p

fn = "/Users/mlandis/projects/mxra8_bovinae/analyses/mxra8_insert_dnds/plot/EDF12_dnds.pdf"
pdf(height=4,width=4.5,file=fn)
print(p)
dev.off()
