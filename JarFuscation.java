import org.objectweb.asm.*;
import org.objectweb.asm.tree.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.jar.*;

public class JarFuscation {

static Random rand = new Random();

static int randInt(int min,int max){return rand.nextInt(max-min)+min;}
static String randName(){String c="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";String s="";for(int i=0;i<6;i++)s+=c.charAt(rand.nextInt(c.length()));return s;}

static int[] encrypt(String s,int key){
int[] out=new int[s.length()];
for(int i=0;i<s.length();i++)out[i]=s.charAt(i)^key;
return out;
}

static InsnList decryptCall(int[] enc){
InsnList list=new InsnList();
list.add(new IntInsnNode(Opcodes.BIPUSH,enc.length));
list.add(new IntInsnNode(Opcodes.NEWARRAY,Opcodes.T_INT));
for(int i=0;i<enc.length;i++){
list.add(new InsnNode(Opcodes.DUP));
list.add(new IntInsnNode(Opcodes.BIPUSH,i));
list.add(new IntInsnNode(Opcodes.SIPUSH,enc[i]));
list.add(new InsnNode(Opcodes.IASTORE));
}
list.add(new MethodInsnNode(Opcodes.INVOKESTATIC,"StringVault","d","([I)Ljava/lang/String;",false));
return list;
}

static byte[] transform(byte[] input){
try{
ClassNode cn=new ClassNode();
new ClassReader(input).accept(cn,0);
cn.name="_"+randName().toUpperCase();
cn.methods.forEach(mn->{mn.name="_"+randName().toUpperCase();mn.access=Opcodes.ACC_PRIVATE|Opcodes.ACC_STATIC;});
cn.fields.forEach(fn->{fn.name="_"+randName().toUpperCase();fn.access=Opcodes.ACC_PRIVATE|Opcodes.ACC_STATIC|Opcodes.ACC_FINAL;});

cn.methods.forEach(mn->{
ListIterator<AbstractInsnNode> it=mn.instructions.iterator();
while(it.hasNext()){
AbstractInsnNode insn=it.next();
if(insn instanceof LdcInsnNode ldc && ldc.cst instanceof String s && s.length()>1){
int key=randInt(5,255);
mn.instructions.insert(insn,decryptCall(encrypt(s,key)));
mn.instructions.remove(insn);
}}
InsnList junk=new InsnList();
junk.add(new MethodInsnNode(Opcodes.INVOKESTATIC,"java/lang/System","nanoTime","()J",false));
junk.add(new InsnNode(Opcodes.POP2));
mn.instructions.insert(junk);
if(rand.nextBoolean()){LabelNode l1=new LabelNode(),l2=new LabelNode();InsnList cf=new InsnList();cf.add(new JumpInsnNode(Opcodes.GOTO,l1));cf.add(l2);cf.add(l1);mn.instructions.insert(cf);}
});
cn.sourceFile=null;
ClassWriter cw=new ClassWriter(ClassWriter.COMPUTE_FRAMES);
cn.accept(cw);
return cw.toByteArray();
}catch(Exception ex){ex.printStackTrace();return input;}
}

static byte[] createVault() throws Exception{
int key=randInt(5,255);
String src="public class StringVault{public static String d(int[] d){char[] o=new char[d.length];for(int i=0;i<d.length;i++)o[i]=(char)(d[i]^"+key+");return new String(o);}}";
Path tmp=Files.createTempDirectory("obf_vault");
Path p=tmp.resolve("StringVault.java");
Files.writeString(p,src);
Process javac=new ProcessBuilder("javac",p.toString()).start();
javac.waitFor();javac.getInputStream().close();javac.getOutputStream().close();javac.getErrorStream().close();
byte[] b=Files.readAllBytes(tmp.resolve("StringVault.class"));
Files.delete(p);Files.delete(tmp.resolve("StringVault.class"));Files.delete(tmp);
return b;
}

static void addFakeClasses(JarOutputStream out) throws Exception{
Path tmp=Files.createTempDirectory("obf_fake");
for(int i=0;i<5;i++){
String clsName="_"+randName().toUpperCase();
String methodName="_"+randName().toUpperCase();
String cls="public class "+clsName+"{public void "+methodName+"(){int x=0;if(x==0)x++;try{int y=1/1;}catch(Exception e){}}}";
Path javaFile=tmp.resolve(clsName+".java");
Files.writeString(javaFile,cls);
Process javac=new ProcessBuilder("javac",javaFile.toString()).start();
javac.waitFor();javac.getInputStream().close();javac.getOutputStream().close();javac.getErrorStream().close();
byte[] b=Files.readAllBytes(tmp.resolve(clsName+".class"));
out.putNextEntry(new JarEntry(clsName+".class"));
out.write(b);
Files.delete(javaFile);Files.delete(tmp.resolve(clsName+".class"));
}
Files.delete(tmp);
}

public static void main(String[] args) throws Exception{
JarFile jar=new JarFile(args[0]);
JarOutputStream out=new JarOutputStream(new FileOutputStream(args[1]));
Enumeration<JarEntry> e=jar.entries();
while(e.hasMoreElements()){
JarEntry entry=e.nextElement();
InputStream is=jar.getInputStream(entry);
byte[] data=is.readAllBytes();
if(entry.getName().endsWith(".class"))data=transform(data);
out.putNextEntry(new JarEntry(entry.getName()));
out.write(data);
}
out.putNextEntry(new JarEntry("StringVault.class"));
out.write(createVault());
addFakeClasses(out);
out.close();jar.close();
}
}
