package weibo;

/**
 * Created with IntelliJ IDEA.
 * User: lgu
 * Date: 5/19/14
 * Time: 3:09 PM
 * To change this template use File | Settings | File Templates.
 */
public class CallResult {

    boolean result;

    Userinfo userinfo;

    public boolean isResult() {
        return result;
    }

    public void setResult(boolean result) {
        this.result = result;
    }

    public Userinfo getUserinfo() {
        return userinfo;
    }

    public void setUserinfo(Userinfo userinfo) {
        this.userinfo = userinfo;
    }
}
