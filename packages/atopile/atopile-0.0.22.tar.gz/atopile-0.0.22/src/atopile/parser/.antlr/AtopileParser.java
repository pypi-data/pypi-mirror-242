// Generated from /Users/mattwildoer/Projects/atopile-workspace/atopile/src/atopile/parser/AtopileParser.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class AtopileParser extends AtopileParserBase {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		INDENT=1, DEDENT=2, STRING=3, PHYSICAL=4, NUMBER=5, INTEGER=6, COMPONENT=7, 
		MODULE=8, INTERFACE=9, PIN=10, SIGNAL=11, WITH=12, OPTIONAL=13, NEW=14, 
		FROM=15, IMPORT=16, PRIVATE=17, TRUE=18, FALSE=19, NEWLINE=20, NAME=21, 
		STRING_LITERAL=22, BYTES_LITERAL=23, DECIMAL_INTEGER=24, OCT_INTEGER=25, 
		HEX_INTEGER=26, BIN_INTEGER=27, FLOAT_NUMBER=28, IMAG_NUMBER=29, DOT=30, 
		ELLIPSIS=31, STAR=32, OPEN_PAREN=33, CLOSE_PAREN=34, COMMA=35, COLON=36, 
		SEMI_COLON=37, POWER=38, ASSIGN=39, OPEN_BRACK=40, CLOSE_BRACK=41, OR_OP=42, 
		XOR=43, AND_OP=44, LEFT_SHIFT=45, RIGHT_SHIFT=46, ADD=47, MINUS=48, DIV=49, 
		MOD=50, IDIV=51, NOT_OP=52, OPEN_BRACE=53, CLOSE_BRACE=54, LESS_THAN=55, 
		GREATER_THAN=56, EQUALS=57, GT_EQ=58, LT_EQ=59, NOT_EQ_1=60, NOT_EQ_2=61, 
		AT=62, ARROW=63, ADD_ASSIGN=64, SUB_ASSIGN=65, MULT_ASSIGN=66, AT_ASSIGN=67, 
		DIV_ASSIGN=68, MOD_ASSIGN=69, AND_ASSIGN=70, OR_ASSIGN=71, XOR_ASSIGN=72, 
		LEFT_SHIFT_ASSIGN=73, RIGHT_SHIFT_ASSIGN=74, POWER_ASSIGN=75, IDIV_ASSIGN=76, 
		SKIP_=77, UNKNOWN_CHAR=78, UNDEFINED=79;
	public static final int
		RULE_file_input = 0, RULE_stmt = 1, RULE_simple_stmts = 2, RULE_simple_stmt = 3, 
		RULE_compound_stmt = 4, RULE_block = 5, RULE_blockdef = 6, RULE_blocktype = 7, 
		RULE_import_stmt = 8, RULE_assign_stmt = 9, RULE_assignable = 10, RULE_retype_stmt = 11, 
		RULE_connect_stmt = 12, RULE_connectable = 13, RULE_signaldef_stmt = 14, 
		RULE_pindef_stmt = 15, RULE_with_stmt = 16, RULE_new_stmt = 17, RULE_name_or_attr = 18, 
		RULE_numerical_pin_ref = 19, RULE_attr = 20, RULE_totally_an_integer = 21, 
		RULE_name = 22, RULE_string = 23, RULE_boolean_ = 24;
	private static String[] makeRuleNames() {
		return new String[] {
			"file_input", "stmt", "simple_stmts", "simple_stmt", "compound_stmt", 
			"block", "blockdef", "blocktype", "import_stmt", "assign_stmt", "assignable", 
			"retype_stmt", "connect_stmt", "connectable", "signaldef_stmt", "pindef_stmt", 
			"with_stmt", "new_stmt", "name_or_attr", "numerical_pin_ref", "attr", 
			"totally_an_integer", "name", "string", "boolean_"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, null, null, null, null, null, null, "'component'", "'module'", 
			"'interface'", "'pin'", "'signal'", "'with'", "'optional'", "'new'", 
			"'from'", "'import'", "'private'", "'True'", "'False'", null, null, null, 
			null, null, null, null, null, null, null, "'.'", "'...'", "'*'", "'('", 
			"')'", "','", "':'", "';'", "'**'", "'='", "'['", "']'", "'|'", "'^'", 
			"'&'", "'<<'", "'>>'", "'+'", "'-'", "'/'", "'%'", "'//'", "'~'", "'{'", 
			"'}'", "'<'", "'>'", "'=='", "'>='", "'<='", "'<>'", "'!='", "'@'", "'->'", 
			"'+='", "'-='", "'*='", "'@='", "'/='", "'%='", "'&='", "'|='", "'^='", 
			"'<<='", "'>>='", "'**='", "'//='"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "INDENT", "DEDENT", "STRING", "PHYSICAL", "NUMBER", "INTEGER", 
			"COMPONENT", "MODULE", "INTERFACE", "PIN", "SIGNAL", "WITH", "OPTIONAL", 
			"NEW", "FROM", "IMPORT", "PRIVATE", "TRUE", "FALSE", "NEWLINE", "NAME", 
			"STRING_LITERAL", "BYTES_LITERAL", "DECIMAL_INTEGER", "OCT_INTEGER", 
			"HEX_INTEGER", "BIN_INTEGER", "FLOAT_NUMBER", "IMAG_NUMBER", "DOT", "ELLIPSIS", 
			"STAR", "OPEN_PAREN", "CLOSE_PAREN", "COMMA", "COLON", "SEMI_COLON", 
			"POWER", "ASSIGN", "OPEN_BRACK", "CLOSE_BRACK", "OR_OP", "XOR", "AND_OP", 
			"LEFT_SHIFT", "RIGHT_SHIFT", "ADD", "MINUS", "DIV", "MOD", "IDIV", "NOT_OP", 
			"OPEN_BRACE", "CLOSE_BRACE", "LESS_THAN", "GREATER_THAN", "EQUALS", "GT_EQ", 
			"LT_EQ", "NOT_EQ_1", "NOT_EQ_2", "AT", "ARROW", "ADD_ASSIGN", "SUB_ASSIGN", 
			"MULT_ASSIGN", "AT_ASSIGN", "DIV_ASSIGN", "MOD_ASSIGN", "AND_ASSIGN", 
			"OR_ASSIGN", "XOR_ASSIGN", "LEFT_SHIFT_ASSIGN", "RIGHT_SHIFT_ASSIGN", 
			"POWER_ASSIGN", "IDIV_ASSIGN", "SKIP_", "UNKNOWN_CHAR", "UNDEFINED"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "AtopileParser.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public AtopileParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class File_inputContext extends ParserRuleContext {
		public TerminalNode EOF() { return getToken(AtopileParser.EOF, 0); }
		public List<TerminalNode> NEWLINE() { return getTokens(AtopileParser.NEWLINE); }
		public TerminalNode NEWLINE(int i) {
			return getToken(AtopileParser.NEWLINE, i);
		}
		public List<StmtContext> stmt() {
			return getRuleContexts(StmtContext.class);
		}
		public StmtContext stmt(int i) {
			return getRuleContext(StmtContext.class,i);
		}
		public File_inputContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_file_input; }
	}

	public final File_inputContext file_input() throws RecognitionException {
		File_inputContext _localctx = new File_inputContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_file_input);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(54);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << COMPONENT) | (1L << MODULE) | (1L << INTERFACE) | (1L << PIN) | (1L << SIGNAL) | (1L << WITH) | (1L << IMPORT) | (1L << PRIVATE) | (1L << NEWLINE) | (1L << NAME))) != 0)) {
				{
				setState(52);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case NEWLINE:
					{
					setState(50);
					match(NEWLINE);
					}
					break;
				case COMPONENT:
				case MODULE:
				case INTERFACE:
				case PIN:
				case SIGNAL:
				case WITH:
				case IMPORT:
				case PRIVATE:
				case NAME:
					{
					setState(51);
					stmt();
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(56);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(57);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class StmtContext extends ParserRuleContext {
		public Simple_stmtsContext simple_stmts() {
			return getRuleContext(Simple_stmtsContext.class,0);
		}
		public Compound_stmtContext compound_stmt() {
			return getRuleContext(Compound_stmtContext.class,0);
		}
		public StmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stmt; }
	}

	public final StmtContext stmt() throws RecognitionException {
		StmtContext _localctx = new StmtContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_stmt);
		try {
			setState(61);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case PIN:
			case SIGNAL:
			case WITH:
			case IMPORT:
			case PRIVATE:
			case NAME:
				enterOuterAlt(_localctx, 1);
				{
				setState(59);
				simple_stmts();
				}
				break;
			case COMPONENT:
			case MODULE:
			case INTERFACE:
				enterOuterAlt(_localctx, 2);
				{
				setState(60);
				compound_stmt();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Simple_stmtsContext extends ParserRuleContext {
		public List<Simple_stmtContext> simple_stmt() {
			return getRuleContexts(Simple_stmtContext.class);
		}
		public Simple_stmtContext simple_stmt(int i) {
			return getRuleContext(Simple_stmtContext.class,i);
		}
		public TerminalNode NEWLINE() { return getToken(AtopileParser.NEWLINE, 0); }
		public List<TerminalNode> SEMI_COLON() { return getTokens(AtopileParser.SEMI_COLON); }
		public TerminalNode SEMI_COLON(int i) {
			return getToken(AtopileParser.SEMI_COLON, i);
		}
		public Simple_stmtsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_simple_stmts; }
	}

	public final Simple_stmtsContext simple_stmts() throws RecognitionException {
		Simple_stmtsContext _localctx = new Simple_stmtsContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_simple_stmts);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(63);
			simple_stmt();
			setState(68);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(64);
					match(SEMI_COLON);
					setState(65);
					simple_stmt();
					}
					} 
				}
				setState(70);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			}
			setState(72);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==SEMI_COLON) {
				{
				setState(71);
				match(SEMI_COLON);
				}
			}

			setState(74);
			match(NEWLINE);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Simple_stmtContext extends ParserRuleContext {
		public Import_stmtContext import_stmt() {
			return getRuleContext(Import_stmtContext.class,0);
		}
		public Assign_stmtContext assign_stmt() {
			return getRuleContext(Assign_stmtContext.class,0);
		}
		public Connect_stmtContext connect_stmt() {
			return getRuleContext(Connect_stmtContext.class,0);
		}
		public Retype_stmtContext retype_stmt() {
			return getRuleContext(Retype_stmtContext.class,0);
		}
		public Pindef_stmtContext pindef_stmt() {
			return getRuleContext(Pindef_stmtContext.class,0);
		}
		public Signaldef_stmtContext signaldef_stmt() {
			return getRuleContext(Signaldef_stmtContext.class,0);
		}
		public With_stmtContext with_stmt() {
			return getRuleContext(With_stmtContext.class,0);
		}
		public Simple_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_simple_stmt; }
	}

	public final Simple_stmtContext simple_stmt() throws RecognitionException {
		Simple_stmtContext _localctx = new Simple_stmtContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_simple_stmt);
		try {
			setState(83);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(76);
				import_stmt();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(77);
				assign_stmt();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(78);
				connect_stmt();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(79);
				retype_stmt();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(80);
				pindef_stmt();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(81);
				signaldef_stmt();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(82);
				with_stmt();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Compound_stmtContext extends ParserRuleContext {
		public BlockdefContext blockdef() {
			return getRuleContext(BlockdefContext.class,0);
		}
		public Compound_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_compound_stmt; }
	}

	public final Compound_stmtContext compound_stmt() throws RecognitionException {
		Compound_stmtContext _localctx = new Compound_stmtContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_compound_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(85);
			blockdef();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BlockContext extends ParserRuleContext {
		public Simple_stmtsContext simple_stmts() {
			return getRuleContext(Simple_stmtsContext.class,0);
		}
		public TerminalNode NEWLINE() { return getToken(AtopileParser.NEWLINE, 0); }
		public TerminalNode INDENT() { return getToken(AtopileParser.INDENT, 0); }
		public TerminalNode DEDENT() { return getToken(AtopileParser.DEDENT, 0); }
		public List<StmtContext> stmt() {
			return getRuleContexts(StmtContext.class);
		}
		public StmtContext stmt(int i) {
			return getRuleContext(StmtContext.class,i);
		}
		public BlockContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_block; }
	}

	public final BlockContext block() throws RecognitionException {
		BlockContext _localctx = new BlockContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_block);
		int _la;
		try {
			setState(97);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case PIN:
			case SIGNAL:
			case WITH:
			case IMPORT:
			case PRIVATE:
			case NAME:
				enterOuterAlt(_localctx, 1);
				{
				setState(87);
				simple_stmts();
				}
				break;
			case NEWLINE:
				enterOuterAlt(_localctx, 2);
				{
				setState(88);
				match(NEWLINE);
				setState(89);
				match(INDENT);
				setState(91); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(90);
					stmt();
					}
					}
					setState(93); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << COMPONENT) | (1L << MODULE) | (1L << INTERFACE) | (1L << PIN) | (1L << SIGNAL) | (1L << WITH) | (1L << IMPORT) | (1L << PRIVATE) | (1L << NAME))) != 0) );
				setState(95);
				match(DEDENT);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BlockdefContext extends ParserRuleContext {
		public BlocktypeContext blocktype() {
			return getRuleContext(BlocktypeContext.class,0);
		}
		public NameContext name() {
			return getRuleContext(NameContext.class,0);
		}
		public TerminalNode COLON() { return getToken(AtopileParser.COLON, 0); }
		public BlockContext block() {
			return getRuleContext(BlockContext.class,0);
		}
		public TerminalNode FROM() { return getToken(AtopileParser.FROM, 0); }
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public BlockdefContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_blockdef; }
	}

	public final BlockdefContext blockdef() throws RecognitionException {
		BlockdefContext _localctx = new BlockdefContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_blockdef);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(99);
			blocktype();
			setState(100);
			name();
			setState(103);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==FROM) {
				{
				setState(101);
				match(FROM);
				setState(102);
				name_or_attr();
				}
			}

			setState(105);
			match(COLON);
			setState(106);
			block();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class BlocktypeContext extends ParserRuleContext {
		public TerminalNode COMPONENT() { return getToken(AtopileParser.COMPONENT, 0); }
		public TerminalNode MODULE() { return getToken(AtopileParser.MODULE, 0); }
		public TerminalNode INTERFACE() { return getToken(AtopileParser.INTERFACE, 0); }
		public BlocktypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_blocktype; }
	}

	public final BlocktypeContext blocktype() throws RecognitionException {
		BlocktypeContext _localctx = new BlocktypeContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_blocktype);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(108);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << COMPONENT) | (1L << MODULE) | (1L << INTERFACE))) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Import_stmtContext extends ParserRuleContext {
		public TerminalNode IMPORT() { return getToken(AtopileParser.IMPORT, 0); }
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public TerminalNode FROM() { return getToken(AtopileParser.FROM, 0); }
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public Import_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_import_stmt; }
	}

	public final Import_stmtContext import_stmt() throws RecognitionException {
		Import_stmtContext _localctx = new Import_stmtContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_import_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(110);
			match(IMPORT);
			setState(111);
			name_or_attr();
			setState(112);
			match(FROM);
			setState(113);
			string();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Assign_stmtContext extends ParserRuleContext {
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public TerminalNode ASSIGN() { return getToken(AtopileParser.ASSIGN, 0); }
		public AssignableContext assignable() {
			return getRuleContext(AssignableContext.class,0);
		}
		public Assign_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assign_stmt; }
	}

	public final Assign_stmtContext assign_stmt() throws RecognitionException {
		Assign_stmtContext _localctx = new Assign_stmtContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_assign_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(115);
			name_or_attr();
			setState(116);
			match(ASSIGN);
			setState(117);
			assignable();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AssignableContext extends ParserRuleContext {
		public StringContext string() {
			return getRuleContext(StringContext.class,0);
		}
		public TerminalNode NUMBER() { return getToken(AtopileParser.NUMBER, 0); }
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public New_stmtContext new_stmt() {
			return getRuleContext(New_stmtContext.class,0);
		}
		public Boolean_Context boolean_() {
			return getRuleContext(Boolean_Context.class,0);
		}
		public TerminalNode PHYSICAL() { return getToken(AtopileParser.PHYSICAL, 0); }
		public TerminalNode UNDEFINED() { return getToken(AtopileParser.UNDEFINED, 0); }
		public AssignableContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_assignable; }
	}

	public final AssignableContext assignable() throws RecognitionException {
		AssignableContext _localctx = new AssignableContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_assignable);
		try {
			setState(126);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(119);
				string();
				}
				break;
			case NUMBER:
				enterOuterAlt(_localctx, 2);
				{
				setState(120);
				match(NUMBER);
				}
				break;
			case NAME:
				enterOuterAlt(_localctx, 3);
				{
				setState(121);
				name_or_attr();
				}
				break;
			case NEW:
				enterOuterAlt(_localctx, 4);
				{
				setState(122);
				new_stmt();
				}
				break;
			case TRUE:
			case FALSE:
				enterOuterAlt(_localctx, 5);
				{
				setState(123);
				boolean_();
				}
				break;
			case PHYSICAL:
				enterOuterAlt(_localctx, 6);
				{
				setState(124);
				match(PHYSICAL);
				}
				break;
			case UNDEFINED:
				enterOuterAlt(_localctx, 7);
				{
				setState(125);
				match(UNDEFINED);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Retype_stmtContext extends ParserRuleContext {
		public List<Name_or_attrContext> name_or_attr() {
			return getRuleContexts(Name_or_attrContext.class);
		}
		public Name_or_attrContext name_or_attr(int i) {
			return getRuleContext(Name_or_attrContext.class,i);
		}
		public TerminalNode ARROW() { return getToken(AtopileParser.ARROW, 0); }
		public Retype_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_retype_stmt; }
	}

	public final Retype_stmtContext retype_stmt() throws RecognitionException {
		Retype_stmtContext _localctx = new Retype_stmtContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_retype_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(128);
			name_or_attr();
			setState(129);
			match(ARROW);
			setState(130);
			name_or_attr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Connect_stmtContext extends ParserRuleContext {
		public List<ConnectableContext> connectable() {
			return getRuleContexts(ConnectableContext.class);
		}
		public ConnectableContext connectable(int i) {
			return getRuleContext(ConnectableContext.class,i);
		}
		public TerminalNode NOT_OP() { return getToken(AtopileParser.NOT_OP, 0); }
		public Connect_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_connect_stmt; }
	}

	public final Connect_stmtContext connect_stmt() throws RecognitionException {
		Connect_stmtContext _localctx = new Connect_stmtContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_connect_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(132);
			connectable();
			setState(133);
			match(NOT_OP);
			setState(134);
			connectable();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class ConnectableContext extends ParserRuleContext {
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public Numerical_pin_refContext numerical_pin_ref() {
			return getRuleContext(Numerical_pin_refContext.class,0);
		}
		public Signaldef_stmtContext signaldef_stmt() {
			return getRuleContext(Signaldef_stmtContext.class,0);
		}
		public Pindef_stmtContext pindef_stmt() {
			return getRuleContext(Pindef_stmtContext.class,0);
		}
		public ConnectableContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_connectable; }
	}

	public final ConnectableContext connectable() throws RecognitionException {
		ConnectableContext _localctx = new ConnectableContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_connectable);
		try {
			setState(140);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,10,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(136);
				name_or_attr();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(137);
				numerical_pin_ref();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(138);
				signaldef_stmt();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(139);
				pindef_stmt();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Signaldef_stmtContext extends ParserRuleContext {
		public TerminalNode SIGNAL() { return getToken(AtopileParser.SIGNAL, 0); }
		public NameContext name() {
			return getRuleContext(NameContext.class,0);
		}
		public TerminalNode PRIVATE() { return getToken(AtopileParser.PRIVATE, 0); }
		public Signaldef_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_signaldef_stmt; }
	}

	public final Signaldef_stmtContext signaldef_stmt() throws RecognitionException {
		Signaldef_stmtContext _localctx = new Signaldef_stmtContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_signaldef_stmt);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(143);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==PRIVATE) {
				{
				setState(142);
				match(PRIVATE);
				}
			}

			setState(145);
			match(SIGNAL);
			setState(146);
			name();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Pindef_stmtContext extends ParserRuleContext {
		public TerminalNode PIN() { return getToken(AtopileParser.PIN, 0); }
		public NameContext name() {
			return getRuleContext(NameContext.class,0);
		}
		public Totally_an_integerContext totally_an_integer() {
			return getRuleContext(Totally_an_integerContext.class,0);
		}
		public Pindef_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_pindef_stmt; }
	}

	public final Pindef_stmtContext pindef_stmt() throws RecognitionException {
		Pindef_stmtContext _localctx = new Pindef_stmtContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_pindef_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(148);
			match(PIN);
			setState(151);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NAME:
				{
				setState(149);
				name();
				}
				break;
			case NUMBER:
				{
				setState(150);
				totally_an_integer();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class With_stmtContext extends ParserRuleContext {
		public TerminalNode WITH() { return getToken(AtopileParser.WITH, 0); }
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public With_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_with_stmt; }
	}

	public final With_stmtContext with_stmt() throws RecognitionException {
		With_stmtContext _localctx = new With_stmtContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_with_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(153);
			match(WITH);
			setState(154);
			name_or_attr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class New_stmtContext extends ParserRuleContext {
		public TerminalNode NEW() { return getToken(AtopileParser.NEW, 0); }
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public New_stmtContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_new_stmt; }
	}

	public final New_stmtContext new_stmt() throws RecognitionException {
		New_stmtContext _localctx = new New_stmtContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_new_stmt);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(156);
			match(NEW);
			setState(157);
			name_or_attr();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Name_or_attrContext extends ParserRuleContext {
		public AttrContext attr() {
			return getRuleContext(AttrContext.class,0);
		}
		public NameContext name() {
			return getRuleContext(NameContext.class,0);
		}
		public Name_or_attrContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_name_or_attr; }
	}

	public final Name_or_attrContext name_or_attr() throws RecognitionException {
		Name_or_attrContext _localctx = new Name_or_attrContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_name_or_attr);
		try {
			setState(161);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,13,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(159);
				attr();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(160);
				name();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Numerical_pin_refContext extends ParserRuleContext {
		public Name_or_attrContext name_or_attr() {
			return getRuleContext(Name_or_attrContext.class,0);
		}
		public TerminalNode DOT() { return getToken(AtopileParser.DOT, 0); }
		public Totally_an_integerContext totally_an_integer() {
			return getRuleContext(Totally_an_integerContext.class,0);
		}
		public Numerical_pin_refContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_numerical_pin_ref; }
	}

	public final Numerical_pin_refContext numerical_pin_ref() throws RecognitionException {
		Numerical_pin_refContext _localctx = new Numerical_pin_refContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_numerical_pin_ref);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(163);
			name_or_attr();
			setState(164);
			match(DOT);
			setState(165);
			totally_an_integer();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class AttrContext extends ParserRuleContext {
		public List<NameContext> name() {
			return getRuleContexts(NameContext.class);
		}
		public NameContext name(int i) {
			return getRuleContext(NameContext.class,i);
		}
		public List<TerminalNode> DOT() { return getTokens(AtopileParser.DOT); }
		public TerminalNode DOT(int i) {
			return getToken(AtopileParser.DOT, i);
		}
		public AttrContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_attr; }
	}

	public final AttrContext attr() throws RecognitionException {
		AttrContext _localctx = new AttrContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_attr);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(167);
			name();
			setState(170); 
			_errHandler.sync(this);
			_alt = 1;
			do {
				switch (_alt) {
				case 1:
					{
					{
					setState(168);
					match(DOT);
					setState(169);
					name();
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				setState(172); 
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,14,_ctx);
			} while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Totally_an_integerContext extends ParserRuleContext {
		public TerminalNode NUMBER() { return getToken(AtopileParser.NUMBER, 0); }
		public Totally_an_integerContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_totally_an_integer; }
	}

	public final Totally_an_integerContext totally_an_integer() throws RecognitionException {
		Totally_an_integerContext _localctx = new Totally_an_integerContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_totally_an_integer);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(174);
			match(NUMBER);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class NameContext extends ParserRuleContext {
		public TerminalNode NAME() { return getToken(AtopileParser.NAME, 0); }
		public NameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_name; }
	}

	public final NameContext name() throws RecognitionException {
		NameContext _localctx = new NameContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_name);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(176);
			match(NAME);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class StringContext extends ParserRuleContext {
		public TerminalNode STRING() { return getToken(AtopileParser.STRING, 0); }
		public StringContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_string; }
	}

	public final StringContext string() throws RecognitionException {
		StringContext _localctx = new StringContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_string);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(178);
			match(STRING);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static class Boolean_Context extends ParserRuleContext {
		public TerminalNode TRUE() { return getToken(AtopileParser.TRUE, 0); }
		public TerminalNode FALSE() { return getToken(AtopileParser.FALSE, 0); }
		public Boolean_Context(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_boolean_; }
	}

	public final Boolean_Context boolean_() throws RecognitionException {
		Boolean_Context _localctx = new Boolean_Context(_ctx, getState());
		enterRule(_localctx, 48, RULE_boolean_);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(180);
			_la = _input.LA(1);
			if ( !(_la==TRUE || _la==FALSE) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3Q\u00b9\4\2\t\2\4"+
		"\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t"+
		"\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\3\2\3\2\7\2\67\n\2\f\2\16\2:\13\2\3\2\3\2\3\3\3\3\5\3@\n\3"+
		"\3\4\3\4\3\4\7\4E\n\4\f\4\16\4H\13\4\3\4\5\4K\n\4\3\4\3\4\3\5\3\5\3\5"+
		"\3\5\3\5\3\5\3\5\5\5V\n\5\3\6\3\6\3\7\3\7\3\7\3\7\6\7^\n\7\r\7\16\7_\3"+
		"\7\3\7\5\7d\n\7\3\b\3\b\3\b\3\b\5\bj\n\b\3\b\3\b\3\b\3\t\3\t\3\n\3\n\3"+
		"\n\3\n\3\n\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\5\f\u0081\n"+
		"\f\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\5\17\u008f"+
		"\n\17\3\20\5\20\u0092\n\20\3\20\3\20\3\20\3\21\3\21\3\21\5\21\u009a\n"+
		"\21\3\22\3\22\3\22\3\23\3\23\3\23\3\24\3\24\5\24\u00a4\n\24\3\25\3\25"+
		"\3\25\3\25\3\26\3\26\3\26\6\26\u00ad\n\26\r\26\16\26\u00ae\3\27\3\27\3"+
		"\30\3\30\3\31\3\31\3\32\3\32\3\32\2\2\33\2\4\6\b\n\f\16\20\22\24\26\30"+
		"\32\34\36 \"$&(*,.\60\62\2\4\3\2\t\13\3\2\24\25\2\u00ba\28\3\2\2\2\4?"+
		"\3\2\2\2\6A\3\2\2\2\bU\3\2\2\2\nW\3\2\2\2\fc\3\2\2\2\16e\3\2\2\2\20n\3"+
		"\2\2\2\22p\3\2\2\2\24u\3\2\2\2\26\u0080\3\2\2\2\30\u0082\3\2\2\2\32\u0086"+
		"\3\2\2\2\34\u008e\3\2\2\2\36\u0091\3\2\2\2 \u0096\3\2\2\2\"\u009b\3\2"+
		"\2\2$\u009e\3\2\2\2&\u00a3\3\2\2\2(\u00a5\3\2\2\2*\u00a9\3\2\2\2,\u00b0"+
		"\3\2\2\2.\u00b2\3\2\2\2\60\u00b4\3\2\2\2\62\u00b6\3\2\2\2\64\67\7\26\2"+
		"\2\65\67\5\4\3\2\66\64\3\2\2\2\66\65\3\2\2\2\67:\3\2\2\28\66\3\2\2\28"+
		"9\3\2\2\29;\3\2\2\2:8\3\2\2\2;<\7\2\2\3<\3\3\2\2\2=@\5\6\4\2>@\5\n\6\2"+
		"?=\3\2\2\2?>\3\2\2\2@\5\3\2\2\2AF\5\b\5\2BC\7\'\2\2CE\5\b\5\2DB\3\2\2"+
		"\2EH\3\2\2\2FD\3\2\2\2FG\3\2\2\2GJ\3\2\2\2HF\3\2\2\2IK\7\'\2\2JI\3\2\2"+
		"\2JK\3\2\2\2KL\3\2\2\2LM\7\26\2\2M\7\3\2\2\2NV\5\22\n\2OV\5\24\13\2PV"+
		"\5\32\16\2QV\5\30\r\2RV\5 \21\2SV\5\36\20\2TV\5\"\22\2UN\3\2\2\2UO\3\2"+
		"\2\2UP\3\2\2\2UQ\3\2\2\2UR\3\2\2\2US\3\2\2\2UT\3\2\2\2V\t\3\2\2\2WX\5"+
		"\16\b\2X\13\3\2\2\2Yd\5\6\4\2Z[\7\26\2\2[]\7\3\2\2\\^\5\4\3\2]\\\3\2\2"+
		"\2^_\3\2\2\2_]\3\2\2\2_`\3\2\2\2`a\3\2\2\2ab\7\4\2\2bd\3\2\2\2cY\3\2\2"+
		"\2cZ\3\2\2\2d\r\3\2\2\2ef\5\20\t\2fi\5.\30\2gh\7\21\2\2hj\5&\24\2ig\3"+
		"\2\2\2ij\3\2\2\2jk\3\2\2\2kl\7&\2\2lm\5\f\7\2m\17\3\2\2\2no\t\2\2\2o\21"+
		"\3\2\2\2pq\7\22\2\2qr\5&\24\2rs\7\21\2\2st\5\60\31\2t\23\3\2\2\2uv\5&"+
		"\24\2vw\7)\2\2wx\5\26\f\2x\25\3\2\2\2y\u0081\5\60\31\2z\u0081\7\7\2\2"+
		"{\u0081\5&\24\2|\u0081\5$\23\2}\u0081\5\62\32\2~\u0081\7\6\2\2\177\u0081"+
		"\7Q\2\2\u0080y\3\2\2\2\u0080z\3\2\2\2\u0080{\3\2\2\2\u0080|\3\2\2\2\u0080"+
		"}\3\2\2\2\u0080~\3\2\2\2\u0080\177\3\2\2\2\u0081\27\3\2\2\2\u0082\u0083"+
		"\5&\24\2\u0083\u0084\7A\2\2\u0084\u0085\5&\24\2\u0085\31\3\2\2\2\u0086"+
		"\u0087\5\34\17\2\u0087\u0088\7\66\2\2\u0088\u0089\5\34\17\2\u0089\33\3"+
		"\2\2\2\u008a\u008f\5&\24\2\u008b\u008f\5(\25\2\u008c\u008f\5\36\20\2\u008d"+
		"\u008f\5 \21\2\u008e\u008a\3\2\2\2\u008e\u008b\3\2\2\2\u008e\u008c\3\2"+
		"\2\2\u008e\u008d\3\2\2\2\u008f\35\3\2\2\2\u0090\u0092\7\23\2\2\u0091\u0090"+
		"\3\2\2\2\u0091\u0092\3\2\2\2\u0092\u0093\3\2\2\2\u0093\u0094\7\r\2\2\u0094"+
		"\u0095\5.\30\2\u0095\37\3\2\2\2\u0096\u0099\7\f\2\2\u0097\u009a\5.\30"+
		"\2\u0098\u009a\5,\27\2\u0099\u0097\3\2\2\2\u0099\u0098\3\2\2\2\u009a!"+
		"\3\2\2\2\u009b\u009c\7\16\2\2\u009c\u009d\5&\24\2\u009d#\3\2\2\2\u009e"+
		"\u009f\7\20\2\2\u009f\u00a0\5&\24\2\u00a0%\3\2\2\2\u00a1\u00a4\5*\26\2"+
		"\u00a2\u00a4\5.\30\2\u00a3\u00a1\3\2\2\2\u00a3\u00a2\3\2\2\2\u00a4\'\3"+
		"\2\2\2\u00a5\u00a6\5&\24\2\u00a6\u00a7\7 \2\2\u00a7\u00a8\5,\27\2\u00a8"+
		")\3\2\2\2\u00a9\u00ac\5.\30\2\u00aa\u00ab\7 \2\2\u00ab\u00ad\5.\30\2\u00ac"+
		"\u00aa\3\2\2\2\u00ad\u00ae\3\2\2\2\u00ae\u00ac\3\2\2\2\u00ae\u00af\3\2"+
		"\2\2\u00af+\3\2\2\2\u00b0\u00b1\7\7\2\2\u00b1-\3\2\2\2\u00b2\u00b3\7\27"+
		"\2\2\u00b3/\3\2\2\2\u00b4\u00b5\7\5\2\2\u00b5\61\3\2\2\2\u00b6\u00b7\t"+
		"\3\2\2\u00b7\63\3\2\2\2\21\668?FJU_ci\u0080\u008e\u0091\u0099\u00a3\u00ae";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}