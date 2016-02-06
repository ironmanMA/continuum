package com.boomerang.config;

/**
 * @author prateek sachdeva, abhi, mohammad arafath
 */

import java.util.ArrayList;
import javax.servlet.ServletContextEvent;
import javax.servlet.ServletContextListener;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;

public class AppConfigContextListener implements ServletContextListener {
	private static final Logger LOG = LoggerFactory.getLogger(AppConfigContextListener.class);
	private static String HasFilePath = "";

	public void contextInitialized(ServletContextEvent servletContextEvent) {
		String appConfigPath = servletContextEvent.getServletContext().getInitParameter("configPath");
		// String hash_FilePath = servletContextEvent.getServletContext().getInitParameter("hashMD5Path");

		LOG.debug("Config file path{}",appConfigPath);
		if(appConfigPath!=null){
			ArrayList <String> appConfigPaths = new ArrayList<String>();
			appConfigPaths.add(0, appConfigPath);
			// if(  hash_FilePath.equals("null") ){
			// 	hash_FilePath = System.getProperty("user.home")+"/MD5_Hash.properties";
			// }else{
			// 	hash_FilePath +="/MD5_Hash.properties";
			// }
			// System.out.println("Wow in file "+hash_FilePath);
			// appConfigPaths.add(1, hash_FilePath);
			AppConfigLoader.loadConfigs(appConfigPaths);
		}
	}

	public String getFilePath (){
		return "";
	}

	public void contextDestroyed(ServletContextEvent sce) {
	}
}
